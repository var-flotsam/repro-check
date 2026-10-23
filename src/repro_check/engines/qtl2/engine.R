# R/qtl2 genome scan engine.
#
#   Rscript engine.R CONFIG.json
#
# Reads genotype probabilities, a marker map, phenotypes and covariates,
# runs scan1 with a kinship random effect, and writes to config$out_dir:
#   results.json       called peaks, support intervals, founder effects, N per trait
#   lod_profile.csv.gz LOD at every marker for every trait
#   session_info.txt   R and package versions
# The engine never compares anything with a paper; that is compare.py's job.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: Rscript engine.R CONFIG.json")

script_dir <- dirname(normalizePath(sub("^--file=", "",
  grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(script_dir, "lib.R"))
suppressPackageStartupMessages(library(jsonlite))

cfg <- fromJSON(args[1], simplifyVector = TRUE, simplifyDataFrame = FALSE)
dir.create(cfg[["out_dir"]], recursive = TRUE, showWarnings = FALSE)
set.seed(cfg[["seed"]] %||% 1L)

probs <- readRDS(cfg[["genoprobs"]])
map <- readRDS(cfg[["map"]])
id_col <- cfg[["id_column"]] %||% "id"
read_table <- function(path) {
  df <- read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  if (!id_col %in% colnames(df)) stop(sprintf("'%s' has no '%s' column", path, id_col))
  rownames(df) <- df[[id_col]]
  df
}
pheno_df <- read_table(cfg[["pheno"]])
covar_df <- if (!is.null(cfg[["covar"]])) read_table(cfg[["covar"]]) else pheno_df

# Samples: present in genoprobs, phenotypes and covariates, optionally subset.
ids <- Reduce(intersect, list(rownames(probs[[1]]), rownames(pheno_df), rownames(covar_df)))
if (!is.null(cfg[["subset"]])) {
  keep <- as.character(covar_df[ids, cfg[["subset"]][["column"]]]) %in% as.character(cfg[["subset"]][["values"]])
  ids <- ids[keep]
}
if (length(ids) < 10) stop(sprintf("only %d samples in common; check id columns", length(ids)))

# Restrict map and probabilities to the same chromosomes and markers.
chrs <- intersect(names(map), names(probs))
if (!is.null(cfg[["chromosomes"]])) chrs <- intersect(chrs, as.character(cfg[["chromosomes"]]))
map <- map[chrs]
probs <- probs[ids, chrs]
for (chr in chrs) {
  common <- intersect(names(map[[chr]]), dimnames(probs[[chr]])[[3]])
  map[[chr]] <- map[[chr]][common]
  probs[[chr]] <- probs[[chr]][, , common, drop = FALSE]
}

# Phenotype matrix with transforms.
traits <- cfg[["traits"]]
pheno <- matrix(NA_real_, nrow = length(ids), ncol = length(traits),
                dimnames = list(ids, vapply(traits, function(t) t[["name"]], "")))
notes <- list()
for (t in traits) {
  col <- t[["column"]] %||% t[["name"]]
  if (!col %in% colnames(pheno_df)) stop(sprintf("trait column '%s' not found", col))
  x <- transform_trait(pheno_df[ids, col], t[["transform"]] %||% "none")
  if (!is.null(attr(x, "n_nonpositive")) && attr(x, "n_nonpositive") > 0)
    notes[[t[["name"]]]] <- sprintf("%d non-positive values set to NA before log",
                               attr(x, "n_nonpositive"))
  pheno[, t[["name"]]] <- as.numeric(x)
}

addcovar <- build_addcovar(covar_df[ids, , drop = FALSE], cfg[["addcovar"]] %||% character(),
                           cfg[["covar_factors"]] %||% character())
kinship_type <- cfg[["kinship"]] %||% "loco"
kinship <- calc_kinship(probs, type = kinship_type, cores = cfg[["cores"]] %||% 1L)
if (kinship_type == "none") kinship <- NULL

scan <- scan1(probs, pheno, kinship = kinship, addcovar = addcovar,
              cores = cfg[["cores"]] %||% 1L)

peaks <- peaks_with_effects(scan, probs, pheno, kinship, addcovar, map,
                            threshold = cfg[["report_threshold"]] %||% 3,
                            peakdrop = cfg[["peakdrop"]] %||% Inf,
                            drop = cfg[["ci_drop"]] %||% 1.5,
                            effects = cfg[["effects"]] %||% "blup")

perm <- NULL
if ((cfg[["n_perm"]] %||% 0) > 0) {
  set.seed(cfg[["seed"]] %||% 1L)
  operm <- scan1perm(probs, pheno, kinship = kinship, addcovar = addcovar,
                     n_perm = cfg[["n_perm"]], cores = cfg[["cores"]] %||% 1L)
  thr <- summary(operm, alpha = c(0.05, 0.10))
  perm <- lapply(colnames(pheno), function(tr) list(
    alpha_0.05 = unname(thr["0.05", tr]), alpha_0.10 = unname(thr["0.1", tr])))
  names(perm) <- colnames(pheno)
}

write_profile(scan, map, file.path(cfg[["out_dir"]], "lod_profile.csv.gz"))

n_mapped <- lapply(colnames(pheno), function(tr) {
  ok <- !is.na(pheno[, tr])
  if (!is.null(addcovar)) ok <- ok & stats::complete.cases(addcovar)
  sum(ok)
})
names(n_mapped) <- colnames(pheno)

result <- list(
  engine = list(name = "qtl2", r_version = R.version.string,
                qtl2_version = as.character(packageVersion("qtl2"))),
  config = cfg,
  n_samples = length(ids),
  n_markers = sum(vapply(map, length, integer(1))),
  n_mapped = n_mapped,
  addcovar_columns = if (is.null(addcovar)) list() else as.list(colnames(addcovar)),
  notes = notes,
  peaks = peaks,
  permutation_thresholds = perm,
  profile = "lod_profile.csv.gz"
)
writeLines(toJSON(result, auto_unbox = TRUE, digits = NA, null = "null", pretty = TRUE),
           file.path(cfg[["out_dir"]], "results.json"))
writeLines(capture.output(sessionInfo()), file.path(cfg[["out_dir"]], "session_info.txt"))
cat(sprintf("scanned %d traits on %d samples, %d markers; %d peaks\n",
            ncol(pheno), length(ids), result$n_markers, length(peaks)))
