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

filter_vars <- function(data, vars) {
  vars[vars %in% names(data)]
}

build_te <- function(model_obj, data, model_name) {
  valid <- model_obj$model$validObs
  keys <- data[valid, c("anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua")]
  keys$te <- as.numeric(efficiencies(model_obj$model))
  keys$model <- model_name
  keys
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

z_controls_extra <- c(
  "nivel_educacion",
  "credito_obtenido",
  "capacitacion_recibida",
  "asistencia_tecnica_recibida",
  "usuario_agua",
  "asociacion_miembro"
)

controls_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_controls.csv")
controls_table <- NULL
if (file.exists(controls_path)) {
  controls <- read.csv(controls_path, stringsAsFactors = FALSE)
  controls_numeric <- c(
    "valor_total",
    "area_total_ha",
    "labor_total",
    "input_costs",
    "diversificacion_area",
    "shannon_area",
    "num_crops_area",
    "gasto_semilla",
    "gasto_agua_riego",
    "gasto_compra_maquinaria",
    "gasto_compra_equipos",
    "gasto_alquiler_mant_equipos",
    "riego_tecnificado_any",
    "nivel_educacion",
    "credito_obtenido",
    "capacitacion_recibida",
    "asistencia_tecnica_recibida",
    "usuario_agua",
    "asociacion_miembro"
  )
  for (v in controls_numeric) {
    if (v %in% names(controls)) {
      controls[[v]] <- suppressWarnings(as.numeric(controls[[v]]))
    }
  }

  controls <- controls[controls$valor_total > 0 & controls$area_total_ha > 0, ]
  controls <- controls[!is.na(controls$diversificacion_area) & !is.na(controls$size_cat) & !is.na(controls$region_natural), ]

  controls$log_y <- log(controls$valor_total)
  controls$log_land <- log(controls$area_total_ha)
  controls$log_labor <- log(controls$labor_total + 1)
  controls$log_inputs <- log(controls$input_costs + 1)
  controls$log_seed <- log(controls$gasto_semilla + 1)
  controls$log_irrigation_cost <- log(controls$gasto_agua_riego + 1)
  controls$capital_total <- rowSums(
    controls[, c("gasto_compra_maquinaria", "gasto_compra_equipos", "gasto_alquiler_mant_equipos")],
    na.rm = TRUE
  )
  controls$log_capital <- log(controls$capital_total + 1)

  controls$size_cat <- factor(controls$size_cat)
  controls$region_natural <- factor(controls$region_natural)
  controls$size_mediano <- as.integer(controls$size_cat == "mediano_2_5ha")
  controls$size_grande <- as.integer(controls$size_cat == "grande_>5ha")
  controls$diversif_mediano <- controls$diversificacion_area * controls$size_mediano
  controls$diversif_grande <- controls$diversificacion_area * controls$size_grande

  controls_region_dummies <- model.matrix(~ region_natural, data = controls)
  if (ncol(controls_region_dummies) > 1) {
    controls_region_dummies <- controls_region_dummies[, -1, drop = FALSE]
  }
  controls <- cbind(controls, controls_region_dummies)

  x_controls <- c(
    "log_land",
    "log_labor",
    "log_inputs",
    colnames(controls_region_dummies),
    "log_seed",
    "log_irrigation_cost",
    "log_capital",
    "riego_tecnificado_any"
  )
  x_controls <- filter_vars(controls, x_controls)
  z_controls <- filter_vars(controls, c(z_names_main, z_controls_extra))

  controls_model <- safe_frontier(controls, x_controls, z_controls, "controls_ena")
  if (!is.null(controls_model)) {
    controls_table <- tidy_frontier(controls_model$model, controls_model$name)
    write.csv(controls_table, file.path(out_tables, "13_sfa_with_controls_ena.csv"), row.names = FALSE)
    writeLines(
      paste(
        "|", paste(names(controls_table), collapse = " | "), "|",
        "\n|", paste(rep("---", ncol(controls_table)), collapse = " | "), "|",
        "\n",
        paste(apply(controls_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
      ),
      con = file.path(out_tables, "13_sfa_with_controls_ena.md")
    )

    te_controls <- build_te(controls_model, controls, "controls_ena")
    te_controls_csv <- file.path(out_data, "ena2024_with_TE_controls.csv")
    write.csv(te_controls, te_controls_csv, row.names = FALSE)
    te_controls_parquet <- file.path(out_data, "ena2024_with_TE_controls.parquet")
    py_cmd_controls <- sprintf(
      "import pandas as pd; df=pd.read_csv(r'%s'); df.to_parquet(r'%s', index=False)",
      te_controls_csv,
      te_controls_parquet
    )
    system2("python", c("-c", shQuote(py_cmd_controls)))
  }
}

geo2_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_geo2.csv")
temp_topo_table <- NULL
if (file.exists(geo2_path)) {
  geo2 <- read.csv(geo2_path, stringsAsFactors = FALSE)
  geo2_numeric <- c(
    "valor_total",
    "area_total_ha",
    "labor_total",
    "input_costs",
    "diversificacion_area",
    "shannon_area",
    "num_crops_area",
    "prcp_total_z",
    "surface_km2",
    "tmean_2024",
    "tmean_2023",
    "delta_tmean_24_23",
    "elev_m",
    "slope_deg",
    "ruggedness",
    "gasto_semilla",
    "gasto_agua_riego",
    "gasto_compra_maquinaria",
    "gasto_compra_equipos",
    "gasto_alquiler_mant_equipos",
    "riego_tecnificado_any",
    "nivel_educacion",
    "credito_obtenido",
    "capacitacion_recibida",
    "asistencia_tecnica_recibida",
    "usuario_agua",
    "asociacion_miembro"
  )
  for (v in geo2_numeric) {
    if (v %in% names(geo2)) {
      geo2[[v]] <- suppressWarnings(as.numeric(geo2[[v]]))
    }
  }

  geo2 <- geo2[geo2$valor_total > 0 & geo2$area_total_ha > 0, ]
  geo2 <- geo2[!is.na(geo2$diversificacion_area) & !is.na(geo2$size_cat) & !is.na(geo2$region_natural), ]
  geo2 <- geo2[!is.na(geo2$tmean_2024) & !is.na(geo2$elev_m), ]

  geo2$log_y <- log(geo2$valor_total)
  geo2$log_land <- log(geo2$area_total_ha)
  geo2$log_labor <- log(geo2$labor_total + 1)
  geo2$log_inputs <- log(geo2$input_costs + 1)
  geo2$log_seed <- log(geo2$gasto_semilla + 1)
  geo2$log_irrigation_cost <- log(geo2$gasto_agua_riego + 1)
  geo2$capital_total <- rowSums(
    geo2[, c("gasto_compra_maquinaria", "gasto_compra_equipos", "gasto_alquiler_mant_equipos")],
    na.rm = TRUE
  )
  geo2$log_capital <- log(geo2$capital_total + 1)
  geo2$log_surface_km2 <- if ("surface_km2" %in% names(geo2)) log(geo2$surface_km2 + 1) else NA

  geo2$size_cat <- factor(geo2$size_cat)
  geo2$region_natural <- factor(geo2$region_natural)
  geo2$size_mediano <- as.integer(geo2$size_cat == "mediano_2_5ha")
  geo2$size_grande <- as.integer(geo2$size_cat == "grande_>5ha")
  geo2$diversif_mediano <- geo2$diversificacion_area * geo2$size_mediano
  geo2$diversif_grande <- geo2$diversificacion_area * geo2$size_grande

  geo2_region_dummies <- model.matrix(~ region_natural, data = geo2)
  if (ncol(geo2_region_dummies) > 1) {
    geo2_region_dummies <- geo2_region_dummies[, -1, drop = FALSE]
  }
  geo2 <- cbind(geo2, geo2_region_dummies)

  x_geo2_base <- c("log_land", "log_labor", "log_inputs", colnames(geo2_region_dummies))
  if ("surface_km2" %in% names(geo2)) {
    x_geo2_base <- c(x_geo2_base, "log_surface_km2")
  }
  x_geo2_temp <- c(
    x_geo2_base,
    "tmean_2024",
    "delta_tmean_24_23",
    "elev_m",
    "slope_deg",
    "ruggedness",
    "prcp_total_z"
  )
  x_geo2_temp <- filter_vars(geo2, x_geo2_temp)

  geo2_rows <- list()
  model_temp_topo <- safe_frontier(geo2, x_geo2_temp, z_names_main, "temp_topo")
  if (!is.null(model_temp_topo)) {
    geo2_rows[[length(geo2_rows) + 1]] <- tidy_frontier(model_temp_topo$model, model_temp_topo$name)
  }

  x_geo2_controls <- c(x_geo2_temp, "log_seed", "log_irrigation_cost", "log_capital", "riego_tecnificado_any")
  x_geo2_controls <- filter_vars(geo2, x_geo2_controls)
  z_geo2_controls <- filter_vars(geo2, c(z_names_main, z_controls_extra))

  model_controls_temp <- safe_frontier(geo2, x_geo2_controls, z_geo2_controls, "controls_temp_topo")
  if (!is.null(model_controls_temp)) {
    geo2_rows[[length(geo2_rows) + 1]] <- tidy_frontier(model_controls_temp$model, model_controls_temp$name)
  }

  if (length(geo2_rows) > 0) {
    temp_topo_table <- do.call(rbind, geo2_rows)
    write.csv(temp_topo_table, file.path(out_tables, "14_sfa_with_temp_topo.csv"), row.names = FALSE)
    writeLines(
      paste(
        "|", paste(names(temp_topo_table), collapse = " | "), "|",
        "\n|", paste(rep("---", ncol(temp_topo_table)), collapse = " | "), "|",
        "\n",
        paste(apply(temp_topo_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
      ),
      con = file.path(out_tables, "14_sfa_with_temp_topo.md")
    )
  }

  te_geo2_rows <- list()
  if (!is.null(model_temp_topo)) {
    te_geo2_rows[[length(te_geo2_rows) + 1]] <- build_te(model_temp_topo, geo2, "temp_topo")
  }
  if (!is.null(model_controls_temp)) {
    te_geo2_rows[[length(te_geo2_rows) + 1]] <- build_te(model_controls_temp, geo2, "controls_temp_topo")
  }
  if (length(te_geo2_rows) > 0) {
    te_geo2 <- do.call(rbind, te_geo2_rows)
    te_geo2_csv <- file.path(out_data, "ena2024_with_TE_geo2.csv")
    write.csv(te_geo2, te_geo2_csv, row.names = FALSE)
    te_geo2_parquet <- file.path(out_data, "ena2024_with_TE_geo2.parquet")
    py_cmd_geo2 <- sprintf(
      "import pandas as pd; df=pd.read_csv(r'%s'); df.to_parquet(r'%s', index=False)",
      te_geo2_csv,
      te_geo2_parquet
    )
    system2("python", c("-c", shQuote(py_cmd_geo2)))
  }
}

compare_terms_all <- c("Z_diversificacion_area", "Z_diversif_mediano", "Z_diversif_grande")
compare_tables <- list()
compare_tables[[length(compare_tables) + 1]] <- main_table[main_table$term %in% compare_terms_all, c("model", "term", "estimate", "std_error", "p_value")]
if (!is.null(controls_table)) {
  compare_tables[[length(compare_tables) + 1]] <- controls_table[controls_table$term %in% compare_terms_all, c("model", "term", "estimate", "std_error", "p_value")]
}
if (!is.null(temp_topo_table)) {
  compare_tables[[length(compare_tables) + 1]] <- temp_topo_table[temp_topo_table$term %in% compare_terms_all, c("model", "term", "estimate", "std_error", "p_value")]
}
if (length(compare_tables) > 0) {
  compare_all <- do.call(rbind, compare_tables)
  write.csv(compare_all, file.path(out_tables, "15_sfa_compare_effects_all.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(compare_all), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(compare_all)), collapse = " | "), "|",
      "\n",
      paste(apply(compare_all, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "15_sfa_compare_effects_all.md")
  )
}

geo_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_geo.csv")
if (file.exists(geo_path)) {
  geo <- read.csv(geo_path, stringsAsFactors = FALSE)
  geo_numeric <- c(
    "valor_total",
    "area_total_ha",
    "labor_total",
    "input_costs",
    "diversificacion_area",
    "shannon_area",
    "num_crops_area",
    "prcp_total_z",
    "surface_km2"
  )
  for (v in geo_numeric) {
    if (v %in% names(geo)) {
      geo[[v]] <- suppressWarnings(as.numeric(geo[[v]]))
    }
  }

  geo <- geo[geo$valor_total > 0 & geo$area_total_ha > 0, ]
  geo <- geo[!is.na(geo$diversificacion_area) & !is.na(geo$size_cat) & !is.na(geo$region_natural), ]
  geo <- geo[!is.na(geo$prcp_total_z), ]

  geo$log_y <- log(geo$valor_total)
  geo$log_land <- log(geo$area_total_ha)
  geo$log_labor <- log(geo$labor_total + 1)
  geo$log_inputs <- log(geo$input_costs + 1)
  geo$log_surface_km2 <- if ("surface_km2" %in% names(geo)) log(geo$surface_km2 + 1) else NA

  geo$size_cat <- factor(geo$size_cat)
  geo$region_natural <- factor(geo$region_natural)

  geo$size_mediano <- as.integer(geo$size_cat == "mediano_2_5ha")
  geo$size_grande <- as.integer(geo$size_cat == "grande_>5ha")
  geo$diversif_mediano <- geo$diversificacion_area * geo$size_mediano
  geo$diversif_grande <- geo$diversificacion_area * geo$size_grande

  geo_region_dummies <- model.matrix(~ region_natural, data = geo)
  if (ncol(geo_region_dummies) > 1) {
    geo_region_dummies <- geo_region_dummies[, -1, drop = FALSE]
  }
  geo <- cbind(geo, geo_region_dummies)

  x_geo_base <- c("log_land", "log_labor", "log_inputs", colnames(geo_region_dummies))
  if ("surface_km2" %in% names(geo)) {
    x_geo_base <- c(x_geo_base, "log_surface_km2")
  }

  z_geo <- c("diversificacion_area", "size_mediano", "size_grande", "diversif_mediano", "diversif_grande", "prcp_total_z")

  geo_models <- list()
  model_xgeo <- NULL
  model_zgeo <- NULL
  geo_x_names <- c(x_geo_base, "prcp_total_z")
  model_xgeo <- safe_frontier(geo, geo_x_names, z_names_main, "xgeo_prcp")
  if (!is.null(model_xgeo)) {
    geo_models[[length(geo_models) + 1]] <- tidy_frontier(model_xgeo$model, model_xgeo$name)
  }

  model_zgeo <- safe_frontier(geo, x_geo_base, z_geo, "zgeo_prcp")
  if (!is.null(model_zgeo)) {
    geo_models[[length(geo_models) + 1]] <- tidy_frontier(model_zgeo$model, model_zgeo$name)
  }

  if (length(geo_models) > 0) {
    geo_table <- do.call(rbind, geo_models)
    write.csv(geo_table, file.path(out_tables, "07_sfa_with_geo_controls.csv"), row.names = FALSE)
    writeLines(
      paste(
        "|", paste(names(geo_table), collapse = " | "), "|",
        "\n|", paste(rep("---", ncol(geo_table)), collapse = " | "), "|",
        "\n",
        paste(apply(geo_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
      ),
      con = file.path(out_tables, "07_sfa_with_geo_controls.md")
    )

    compare_terms <- c("Z_diversificacion_area", "Z_diversif_mediano", "Z_diversif_grande")
    compare_table <- rbind(
      main_table[main_table$term %in% compare_terms, c("model", "term", "estimate", "std_error", "p_value")],
      geo_table[geo_table$term %in% compare_terms, c("model", "term", "estimate", "std_error", "p_value")]
    )
    write.csv(compare_table, file.path(out_tables, "08_sfa_compare_main_effects.csv"), row.names = FALSE)
    writeLines(
      paste(
        "|", paste(names(compare_table), collapse = " | "), "|",
        "\n|", paste(rep("---", ncol(compare_table)), collapse = " | "), "|",
        "\n",
        paste(apply(compare_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
      ),
      con = file.path(out_tables, "08_sfa_compare_main_effects.md")
    )
  }

  te_geo_rows <- list()
  if (!is.null(model_xgeo)) {
    te_geo_rows[[length(te_geo_rows) + 1]] <- build_te(model_xgeo, geo, "xgeo_prcp")
  }
  if (!is.null(model_zgeo)) {
    te_geo_rows[[length(te_geo_rows) + 1]] <- build_te(model_zgeo, geo, "zgeo_prcp")
  }
  if (length(te_geo_rows) > 0) {
    te_geo <- do.call(rbind, te_geo_rows)
    te_geo_csv <- file.path(out_data, "ena2024_with_TE_geo.csv")
    write.csv(te_geo, te_geo_csv, row.names = FALSE)
    te_geo_parquet <- file.path(out_data, "ena2024_with_TE_geo.parquet")
    py_cmd_geo <- sprintf(
      "import pandas as pd; df=pd.read_csv(r'%s'); df.to_parquet(r'%s', index=False)",
      te_geo_csv,
      te_geo_parquet
    )
    system2("python", c("-c", shQuote(py_cmd_geo)))
  }
}

cat("SFA outputs written to outputs/tables and data/processed.\\n")
