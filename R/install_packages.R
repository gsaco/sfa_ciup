#!/usr/bin/env Rscript
required <- c(
  "frontier",
  "survey",
  "broom",
  "lmtest",
  "zoo"
)

installed <- rownames(installed.packages())
to_install <- setdiff(required, installed)

if (length(to_install) > 0) {
  install.packages(to_install, repos = "https://cloud.r-project.org")
}

cat("R packages ready:", paste(required, collapse = ", "), "\n")
