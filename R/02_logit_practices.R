#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(survey)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg) else ""
repo_root <- normalizePath(file.path(dirname(script_path), ".."))

data_path <- file.path(repo_root, "data", "processed", "model_data_ena2024.csv")
out_tables <- file.path(repo_root, "outputs", "tables")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(data_path, stringsAsFactors = FALSE)

numeric_vars <- c(
  "practice_any",
  "num_practices",
  "diversificacion_area",
  "diversificacion_valor",
  "shannon_area",
  "num_crops_area",
  "area_total_ha",
  "weight"
)
for (v in numeric_vars) {
  if (v %in% names(df)) {
    df[[v]] <- suppressWarnings(as.numeric(df[[v]]))
  }
}

df <- df[!is.na(df$practice_any) & !is.na(df$diversificacion_area) & !is.na(df$weight), ]
df$size_cat <- factor(df$size_cat)
df$region_natural <- factor(df$region_natural)
df$psu <- factor(df$psu)
df$estrato <- factor(df$estrato)
df$log_area <- log(df$area_total_ha + 1)

options(survey.lonely.psu = "adjust")

design <- svydesign(
  ids = ~psu,
  strata = ~estrato,
  weights = ~weight,
  data = df,
  nest = TRUE
)

fit_logit <- function(formula, design, model_name) {
  model <- svyglm(formula, design = design, family = quasibinomial())
  coef_tab <- summary(model)$coefficients
  out <- data.frame(
    model = model_name,
    term = rownames(coef_tab),
    estimate = coef_tab[, 1],
    std_error = coef_tab[, 2],
    z_value = coef_tab[, 3],
    p_value = coef_tab[, 4],
    stringsAsFactors = FALSE
  )
  out$odds_ratio <- exp(out$estimate)
  out
}

main_formula <- practice_any ~ diversificacion_area * size_cat + log_area + region_natural
main_res <- fit_logit(main_formula, design, "main")

write.csv(main_res, file.path(out_tables, "04_logit_main.csv"), row.names = FALSE)
writeLines(
  paste(
    "|", paste(names(main_res), collapse = " | "), "|",
    "\n|", paste(rep("---", ncol(main_res)), collapse = " | "), "|",
    "\n",
    paste(apply(main_res, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
  ),
  con = file.path(out_tables, "04_logit_main.md")
)

robust_rows <- list()

if ("shannon_area" %in% names(df)) {
  df$diversif_alt <- df$shannon_area
  design_alt <- update(design, diversif_alt = df$diversif_alt)
  alt_formula <- practice_any ~ diversif_alt * size_cat + log_area + region_natural
  robust_rows[[length(robust_rows) + 1]] <- fit_logit(alt_formula, design_alt, "alt_shannon")
}

if ("num_crops_area" %in% names(df)) {
  df$diversif_alt2 <- df$num_crops_area
  design_alt2 <- update(design, diversif_alt2 = df$diversif_alt2)
  alt2_formula <- practice_any ~ diversif_alt2 * size_cat + log_area + region_natural
  robust_rows[[length(robust_rows) + 1]] <- fit_logit(alt2_formula, design_alt2, "alt_num_crops")
}

df$practice_two_plus <- as.integer(df$num_practices >= 2)
design_alt3 <- update(design, practice_two_plus = df$practice_two_plus)
alt3_formula <- practice_two_plus ~ diversificacion_area * size_cat + log_area + region_natural
robust_rows[[length(robust_rows) + 1]] <- fit_logit(alt3_formula, design_alt3, "alt_outcome_two_plus")

df_small <- df[df$size_cat == "pequeno_<2ha", ]
if (nrow(df_small) > 0) {
  design_small <- svydesign(
    ids = ~psu,
    strata = ~estrato,
    weights = ~weight,
    data = df_small,
    nest = TRUE
  )
  small_formula <- practice_any ~ diversificacion_area + log_area + region_natural
  robust_rows[[length(robust_rows) + 1]] <- fit_logit(small_formula, design_small, "small_only")
}

robust_table <- do.call(rbind, robust_rows)
write.csv(robust_table, file.path(out_tables, "05_logit_robustness.csv"), row.names = FALSE)
writeLines(
  paste(
    "|", paste(names(robust_table), collapse = " | "), "|",
    "\n|", paste(rep("---", ncol(robust_table)), collapse = " | "), "|",
    "\n",
    paste(apply(robust_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
  ),
  con = file.path(out_tables, "05_logit_robustness.md")
)

cat("Logit outputs written to outputs/tables.\\n")
