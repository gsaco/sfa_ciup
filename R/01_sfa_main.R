#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(frontier)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg) else ""
repo_root <- normalizePath(file.path(dirname(script_path), ".."))
data_path <- file.path(repo_root, "data", "processed", "model_data_ena2024.csv")
out_tables <- file.path(repo_root, "outputs", "tables")
out_data <- file.path(repo_root, "data", "processed")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(data_path, stringsAsFactors = FALSE)

numeric_vars <- c(
  "valor_total",
  "area_total_ha",
  "labor_total",
  "input_costs",
  "diversificacion_area",
  "diversificacion_valor",
  "shannon_area",
  "num_crops_area"
)
for (v in numeric_vars) {
  if (v %in% names(df)) {
    df[[v]] <- suppressWarnings(as.numeric(df[[v]]))
  }
}

df <- df[df$valor_total > 0 & df$area_total_ha > 0, ]
df <- df[!is.na(df$diversificacion_area) & !is.na(df$size_cat) & !is.na(df$region_natural), ]

df$log_y <- log(df$valor_total)
df$log_land <- log(df$area_total_ha)
df$log_labor <- log(df$labor_total + 1)
df$log_inputs <- log(df$input_costs + 1)

df$size_cat <- factor(df$size_cat)
df$region_natural <- factor(df$region_natural)

df$size_mediano <- as.integer(df$size_cat == "mediano_2_5ha")
df$size_grande <- as.integer(df$size_cat == "grande_>5ha")
df$diversif_mediano <- df$diversificacion_area * df$size_mediano
df$diversif_grande <- df$diversificacion_area * df$size_grande

region_dummies <- model.matrix(~ region_natural, data = df)
if (ncol(region_dummies) > 1) {
  region_dummies <- region_dummies[, -1, drop = FALSE]
}
df <- cbind(df, region_dummies)

x_names <- c("log_land", "log_labor", "log_inputs", colnames(region_dummies))
z_names_main <- c("diversificacion_area", "size_mediano", "size_grande", "diversif_mediano", "diversif_grande")

safe_frontier <- function(data, x_names, z_names, model_name) {
  tryCatch(
    {
      model <- frontier(
        yName = "log_y",
        xNames = x_names,
        zNames = z_names,
        data = data,
        zIntercept = TRUE
      )
      list(model = model, name = model_name)
    },
    error = function(e) {
      message(sprintf("Model %s failed: %s", model_name, e$message))
      NULL
    }
  )
}

tidy_frontier <- function(model, model_name) {
  params <- model[["mleParam"]]
  cov <- model[["mleCov"]]
  se <- sqrt(diag(cov))
  z <- params / se
  p <- 2 * (1 - pnorm(abs(z)))
  terms <- names(params)
  component <- ifelse(
    grepl("^Z_", terms),
    "inefficiency",
    ifelse(terms %in% c("sigmaSq", "gamma"), "variance", "frontier")
  )
  data.frame(
    model = model_name,
    term = terms,
    estimate = as.numeric(params),
    std_error = as.numeric(se),
    z_value = as.numeric(z),
    p_value = as.numeric(p),
    component = component,
    stringsAsFactors = FALSE
  )
}

model_main <- safe_frontier(df, x_names, z_names_main, "main_area")
if (is.null(model_main)) {
  stop("Main SFA model failed; cannot proceed.")
}

main_table <- tidy_frontier(model_main$model, model_main$name)
write.csv(main_table, file.path(out_tables, "02_sfa_main.csv"), row.names = FALSE)
writeLines(
  paste(
    "|", paste(names(main_table), collapse = " | "), "|",
    "\n|", paste(rep("---", ncol(main_table)), collapse = " | "), "|",
    "\n",
    paste(apply(main_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
  ),
  con = file.path(out_tables, "02_sfa_main.md")
)

te <- efficiencies(model_main$model)
te_df <- df[, c("anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua")]
te_df$te <- as.numeric(te)
te_csv <- file.path(out_data, "ena2024_with_TE.csv")
write.csv(te_df, te_csv, row.names = FALSE)

te_parquet <- file.path(out_data, "ena2024_with_TE.parquet")
py_cmd <- sprintf(
  "import pandas as pd; df=pd.read_csv(r'%s'); df.to_parquet(r'%s', index=False)",
  te_csv,
  te_parquet
)
system2("python", c("-c", shQuote(py_cmd)))

robust_rows <- list()

if ("shannon_area" %in% names(df)) {
  df$diversif_alt <- df$shannon_area
  df$diversif_alt_med <- df$diversif_alt * df$size_mediano
  df$diversif_alt_gra <- df$diversif_alt * df$size_grande
  z_alt <- c("diversif_alt", "size_mediano", "size_grande", "diversif_alt_med", "diversif_alt_gra")
  alt_model <- safe_frontier(df, x_names, z_alt, "alt_shannon")
  if (!is.null(alt_model)) {
    robust_rows[[length(robust_rows) + 1]] <- tidy_frontier(alt_model$model, alt_model$name)
  }
}

if ("num_crops_area" %in% names(df)) {
  df$diversif_alt2 <- df$num_crops_area
  df$diversif_alt2_med <- df$diversif_alt2 * df$size_mediano
  df$diversif_alt2_gra <- df$diversif_alt2 * df$size_grande
  z_alt2 <- c("diversif_alt2", "size_mediano", "size_grande", "diversif_alt2_med", "diversif_alt2_gra")
  alt2_model <- safe_frontier(df, x_names, z_alt2, "alt_num_crops")
  if (!is.null(alt2_model)) {
    robust_rows[[length(robust_rows) + 1]] <- tidy_frontier(alt2_model$model, alt2_model$name)
  }
}

df_small <- df[df$size_cat == "pequeno_<2ha", ]
if (nrow(df_small) > 0) {
  z_small <- c("diversificacion_area")
  small_model <- safe_frontier(df_small, x_names, z_small, "small_only")
  if (!is.null(small_model)) {
    robust_rows[[length(robust_rows) + 1]] <- tidy_frontier(small_model$model, small_model$name)
  }
}

if (length(robust_rows) > 0) {
  robust_table <- do.call(rbind, robust_rows)
  write.csv(robust_table, file.path(out_tables, "03_sfa_robustness.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(robust_table), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(robust_table)), collapse = " | "), "|",
      "\n",
      paste(apply(robust_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "03_sfa_robustness.md")
  )
}

cat("SFA outputs written to outputs/tables and data/processed.\\n")
