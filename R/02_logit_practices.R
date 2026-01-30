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

controls_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_controls.csv")
controls_res <- NULL
if (file.exists(controls_path)) {
  controls <- read.csv(controls_path, stringsAsFactors = FALSE)
  controls_numeric <- c(
    "practice_any",
    "num_practices",
    "diversificacion_area",
    "area_total_ha",
    "weight",
    "nivel_educacion",
    "capacitacion_recibida",
    "asistencia_tecnica_recibida",
    "usuario_agua",
    "asociacion_miembro",
    "riego_any",
    "uso_maquinaria",
    "usa_abono",
    "usa_fertilizantes",
    "semilla_semillero_any",
    "semilla_comercial_any"
  )
  for (v in controls_numeric) {
    if (v %in% names(controls)) {
      controls[[v]] <- suppressWarnings(as.numeric(controls[[v]]))
    }
  }

  controls <- controls[!is.na(controls$practice_any) & !is.na(controls$diversificacion_area) & !is.na(controls$weight), ]
  controls$size_cat <- factor(controls$size_cat)
  controls$region_natural <- factor(controls$region_natural)
  controls$psu <- factor(controls$psu)
  controls$estrato <- factor(controls$estrato)
  controls$log_area <- log(controls$area_total_ha + 1)

  design_controls <- svydesign(
    ids = ~psu,
    strata = ~estrato,
    weights = ~weight,
    data = controls,
    nest = TRUE
  )

  controls_formula <- practice_any ~ diversificacion_area * size_cat + log_area + region_natural +
    nivel_educacion + capacitacion_recibida + asistencia_tecnica_recibida +
    usuario_agua + asociacion_miembro + riego_any + uso_maquinaria +
    usa_abono + usa_fertilizantes + semilla_semillero_any + semilla_comercial_any
  controls_res <- tryCatch(
    {
      fit_logit(controls_formula, design_controls, "controls_ena")
    },
    error = function(e) {
      alt_formula <- practice_any ~ diversificacion_area * size_cat + log_area +
        nivel_educacion + capacitacion_recibida + asistencia_tecnica_recibida +
        usuario_agua + asociacion_miembro + riego_any + uso_maquinaria +
        usa_abono + usa_fertilizantes + semilla_semillero_any + semilla_comercial_any
      fit_logit(alt_formula, design_controls, "controls_ena_no_region")
    }
  )

  write.csv(controls_res, file.path(out_tables, "16_logit_with_controls_ena.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(controls_res), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(controls_res)), collapse = " | "), "|",
      "\n",
      paste(apply(controls_res, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "16_logit_with_controls_ena.md")
  )
}

geo2_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_geo2.csv")
temp_topo_res <- NULL
controls_temp_topo_res <- NULL
if (file.exists(geo2_path)) {
  geo2 <- read.csv(geo2_path, stringsAsFactors = FALSE)
  geo2_numeric <- c(
    "practice_any",
    "num_practices",
    "diversificacion_area",
    "area_total_ha",
    "weight",
    "prcp_total_z",
    "tmean_2024",
    "tmean_2023",
    "delta_tmean_24_23",
    "elev_m",
    "slope_deg",
    "ruggedness",
    "nivel_educacion",
    "capacitacion_recibida",
    "asistencia_tecnica_recibida",
    "usuario_agua",
    "asociacion_miembro",
    "riego_any",
    "uso_maquinaria",
    "usa_abono",
    "usa_fertilizantes",
    "semilla_semillero_any",
    "semilla_comercial_any"
  )
  for (v in geo2_numeric) {
    if (v %in% names(geo2)) {
      geo2[[v]] <- suppressWarnings(as.numeric(geo2[[v]]))
    }
  }

  geo2 <- geo2[!is.na(geo2$practice_any) & !is.na(geo2$diversificacion_area) & !is.na(geo2$weight), ]
  geo2 <- geo2[!is.na(geo2$tmean_2024) & !is.na(geo2$elev_m), ]
  geo2$size_cat <- factor(geo2$size_cat)
  geo2$region_natural <- factor(geo2$region_natural)
  geo2$psu <- factor(geo2$psu)
  geo2$estrato <- factor(geo2$estrato)
  geo2$log_area <- log(geo2$area_total_ha + 1)

  design_geo2 <- svydesign(
    ids = ~psu,
    strata = ~estrato,
    weights = ~weight,
    data = geo2,
    nest = TRUE
  )

  temp_formula <- practice_any ~ diversificacion_area * size_cat + log_area + region_natural +
    tmean_2024 + delta_tmean_24_23 + elev_m + slope_deg + ruggedness + prcp_total_z
  temp_topo_res <- tryCatch(
    {
      fit_logit(temp_formula, design_geo2, "temp_topo")
    },
    error = function(e) {
      alt_formula <- practice_any ~ diversificacion_area * size_cat + log_area +
        tmean_2024 + delta_tmean_24_23 + elev_m + slope_deg + ruggedness + prcp_total_z
      fit_logit(alt_formula, design_geo2, "temp_topo_no_region")
    }
  )

  controls_temp_formula <- practice_any ~ diversificacion_area * size_cat + log_area + region_natural +
    tmean_2024 + delta_tmean_24_23 + elev_m + slope_deg + ruggedness + prcp_total_z +
    nivel_educacion + capacitacion_recibida + asistencia_tecnica_recibida +
    usuario_agua + asociacion_miembro + riego_any + uso_maquinaria +
    usa_abono + usa_fertilizantes + semilla_semillero_any + semilla_comercial_any
  controls_temp_topo_res <- tryCatch(
    {
      fit_logit(controls_temp_formula, design_geo2, "controls_temp_topo")
    },
    error = function(e) {
      alt_formula <- practice_any ~ diversificacion_area * size_cat + log_area +
        tmean_2024 + delta_tmean_24_23 + elev_m + slope_deg + ruggedness + prcp_total_z +
        nivel_educacion + capacitacion_recibida + asistencia_tecnica_recibida +
        usuario_agua + asociacion_miembro + riego_any + uso_maquinaria +
        usa_abono + usa_fertilizantes + semilla_semillero_any + semilla_comercial_any
      fit_logit(alt_formula, design_geo2, "controls_temp_topo_no_region")
    }
  )

  temp_tables <- rbind(temp_topo_res, controls_temp_topo_res)
  write.csv(temp_tables, file.path(out_tables, "17_logit_with_temp_topo.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(temp_tables), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(temp_tables)), collapse = " | "), "|",
      "\n",
      paste(apply(temp_tables, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "17_logit_with_temp_topo.md")
  )

  compare_terms_all <- c(
    "diversificacion_area",
    "diversificacion_area:size_catmediano_2_5ha",
    "diversificacion_area:size_catpequeno_<2ha"
  )
  compare_rows <- list()
  compare_rows[[length(compare_rows) + 1]] <- main_res[main_res$term %in% compare_terms_all, ]
  if (!is.null(controls_res)) {
    compare_rows[[length(compare_rows) + 1]] <- controls_res[controls_res$term %in% compare_terms_all, ]
  }
  if (!is.null(temp_topo_res)) {
    compare_rows[[length(compare_rows) + 1]] <- temp_topo_res[temp_topo_res$term %in% compare_terms_all, ]
  }
  if (!is.null(controls_temp_topo_res)) {
    compare_rows[[length(compare_rows) + 1]] <- controls_temp_topo_res[controls_temp_topo_res$term %in% compare_terms_all, ]
  }

  if (length(compare_rows) > 0) {
    compare_table <- do.call(rbind, compare_rows)
    write.csv(compare_table, file.path(out_tables, "18_logit_compare_effects_all.csv"), row.names = FALSE)
    writeLines(
      paste(
        "|", paste(names(compare_table), collapse = " | "), "|",
        "\n|", paste(rep("---", ncol(compare_table)), collapse = " | "), "|",
        "\n",
        paste(apply(compare_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
      ),
      con = file.path(out_tables, "18_logit_compare_effects_all.md")
    )
  }
}

geo_path <- file.path(repo_root, "data", "processed", "model_data_ena2024_plus_geo.csv")
if (file.exists(geo_path)) {
  geo <- read.csv(geo_path, stringsAsFactors = FALSE)
  geo_numeric <- c(
    "practice_any",
    "num_practices",
    "diversificacion_area",
    "area_total_ha",
    "weight",
    "prcp_total_z"
  )
  for (v in geo_numeric) {
    if (v %in% names(geo)) {
      geo[[v]] <- suppressWarnings(as.numeric(geo[[v]]))
    }
  }

  geo <- geo[!is.na(geo$practice_any) & !is.na(geo$diversificacion_area) & !is.na(geo$weight), ]
  geo <- geo[!is.na(geo$prcp_total_z), ]
  geo$size_cat <- factor(geo$size_cat)
  geo$region_natural <- factor(geo$region_natural)
  geo$psu <- factor(geo$psu)
  geo$estrato <- factor(geo$estrato)
  geo$log_area <- log(geo$area_total_ha + 1)

  design_geo <- svydesign(
    ids = ~psu,
    strata = ~estrato,
    weights = ~weight,
    data = geo,
    nest = TRUE
  )

  geo_formula <- practice_any ~ diversificacion_area * size_cat + log_area + region_natural + prcp_total_z
  geo_res <- tryCatch(
    {
      fit_logit(geo_formula, design_geo, "main_geo")
    },
    error = function(e) {
      alt_formula <- practice_any ~ diversificacion_area * size_cat + log_area + prcp_total_z
      fit_logit(alt_formula, design_geo, "main_geo_no_region")
    }
  )

  write.csv(geo_res, file.path(out_tables, "09_logit_with_geo_controls.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(geo_res), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(geo_res)), collapse = " | "), "|",
      "\n",
      paste(apply(geo_res, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "09_logit_with_geo_controls.md")
  )

  compare_terms <- c(
    "diversificacion_area",
    "diversificacion_area:size_catmediano_2_5ha",
    "diversificacion_area:size_catpequeno_<2ha"
  )
  compare_table <- rbind(
    main_res[main_res$term %in% compare_terms, ],
    geo_res[geo_res$term %in% compare_terms, ]
  )
  write.csv(compare_table, file.path(out_tables, "10_logit_compare_main_effects.csv"), row.names = FALSE)
  writeLines(
    paste(
      "|", paste(names(compare_table), collapse = " | "), "|",
      "\n|", paste(rep("---", ncol(compare_table)), collapse = " | "), "|",
      "\n",
      paste(apply(compare_table, 1, function(row) paste("|", paste(row, collapse = " | "), "|")), collapse = "\n")
    ),
    con = file.path(out_tables, "10_logit_compare_main_effects.md")
  )
}

cat("Logit outputs written to outputs/tables.\\n")
