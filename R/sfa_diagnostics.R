gamma_diagnostics <- function(model, tol = 0.01) {
  gamma <- NA_real_
  if (!is.null(model$mleParam) && "gamma" %in% names(model$mleParam)) {
    gamma <- as.numeric(model$mleParam["gamma"])
  }
  gamma_near_boundary <- !is.na(gamma) && (gamma < tol || gamma > (1 - tol))
  list(
    gamma = gamma,
    gamma_near_boundary = gamma_near_boundary,
    gamma_tol = tol
  )
}


cov_diagnostics <- function(model) {
  cov_mat <- model$mleCov
  if (is.null(cov_mat)) {
    return(list(cov_singular = TRUE, cov_rank = NA_integer_, cov_cond = NA_real_, cov_rcond = NA_real_))
  }
  cov_mat <- as.matrix(cov_mat)
  if (any(!is.finite(cov_mat))) {
    return(list(cov_singular = TRUE, cov_rank = NA_integer_, cov_cond = NA_real_, cov_rcond = NA_real_))
  }

  cov_rank <- tryCatch(qr(cov_mat)$rank, error = function(e) NA_integer_)
  cov_cond <- tryCatch(kappa(cov_mat), error = function(e) NA_real_)
  cov_rcond <- if (!is.na(cov_cond) && cov_cond > 0) 1 / cov_cond else NA_real_
  inv_ok <- tryCatch({
    solve(cov_mat)
    TRUE
  }, error = function(e) FALSE)

  cov_singular <- !isTRUE(inv_ok) || (!is.na(cov_rank) && cov_rank < ncol(cov_mat))
  list(cov_singular = cov_singular, cov_rank = cov_rank, cov_cond = cov_cond, cov_rcond = cov_rcond)
}


sample_diagnostics <- function(model, data) {
  n_total <- nrow(data)
  n_valid <- if (!is.null(model$validObs)) sum(model$validObs) else NA_integer_
  share_dropped <- if (!is.na(n_valid) && n_total > 0) (n_total - n_valid) / n_total else NA_real_
  list(n_total = n_total, n_valid = n_valid, share_dropped = share_dropped)
}


build_sfa_diagnostics_row <- function(model_obj, data) {
  model <- model_obj$model
  model_name <- model_obj$name
  sample_diag <- sample_diagnostics(model, data)
  gamma_diag <- gamma_diagnostics(model)
  cov_diag <- cov_diagnostics(model)

  data.frame(
    model = model_name,
    n_total = sample_diag$n_total,
    n_valid = sample_diag$n_valid,
    share_dropped = sample_diag$share_dropped,
    gamma = gamma_diag$gamma,
    gamma_near_boundary = gamma_diag$gamma_near_boundary,
    cov_singular = cov_diag$cov_singular,
    cov_rank = cov_diag$cov_rank,
    cov_cond = cov_diag$cov_cond,
    cov_rcond = cov_diag$cov_rcond,
    input_cost_var = NA_character_,
    stringsAsFactors = FALSE
  )
}


attach_diagnostics <- function(table, diagnostics_row) {
  if (is.null(table) || nrow(table) == 0) {
    return(table)
  }
  diag_cols <- setdiff(names(diagnostics_row), "model")
  diag_vals <- diagnostics_row[rep(1, nrow(table)), diag_cols, drop = FALSE]
  cbind(table, diag_vals)
}
