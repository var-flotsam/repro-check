# R/qtl2 engine functions. Sourced by engine.R and simulate.R, and tested
# directly by r/tests/testthat. Kept free of side effects: every function
# takes its inputs as arguments and returns a value.

suppressPackageStartupMessages(library(qtl2))

`%||%` <- function(a, b) if (is.null(a)) b else a

FOUNDERS <- c(A = "AJ", B = "B6", C = "129", D = "NOD",
              E = "NZO", F = "CAST", G = "PWK", H = "WSB")

# Rank-based inverse normal transform; NAs stay NA.
rankz <- function(x) {
  ok <- !is.na(x)
  out <- rep(NA_real_, length(x))
  out[ok] <- qnorm((rank(x[ok]) - 0.5) / sum(ok))
  out
}

# Apply one named transform to a numeric vector.
#   none  : as is
#   log   : natural log; non-positive values become NA (counted and returned)
#   log1p : log(x + 1), for counts
#   rankz : rank inverse normal
transform_trait <- function(x, how) {
  x <- as.numeric(x)
  switch(how,
    none = x,
    log = {
      bad <- !is.na(x) & x <= 0
      x[bad] <- NA
      attr(x, "n_nonpositive") <- sum(bad)
      log(x)
    },
    log1p = log1p(x),
    rankz = rankz(x),
    stop(sprintf("unknown transform '%s' (use none, log, log1p, rankz)", how))
  )
}

# Build the additive covariate matrix. Columns named in `factors` are
# expanded to treatment contrasts (first level dropped); the rest are numeric.
# Rows with any missing covariate are dropped by scan1, so they are kept as NA.
build_addcovar <- function(covar, columns, factors = character()) {
  if (length(columns) == 0) return(NULL)
  missing_cols <- setdiff(columns, colnames(covar))
  if (length(missing_cols) > 0)
    stop("covariate column(s) not found: ", paste(missing_cols, collapse = ", "))
  df <- covar[, columns, drop = FALSE]
  rownames(df) <- NULL
  for (col in columns) {
    if (col %in% factors || is.character(df[[col]])) df[[col]] <- factor(df[[col]])
  }
  # model.matrix drops rows with missing values; put them back as NA rows so
  # the result lines up with the input. Row names of mm are row indices.
  mm <- model.matrix(~ ., data = df)
  out <- matrix(NA_real_, nrow = nrow(df), ncol = ncol(mm) - 1,
                dimnames = list(rownames(covar), colnames(mm)[-1]))
  out[as.integer(rownames(mm)), ] <- mm[, -1, drop = FALSE]
  out
}

# Called peaks with support intervals and founder coefficients at each peak.
#   scan     : scan1 output
#   probs    : genotype probabilities (calc_genoprob / alleleprobs)
#   pheno    : phenotype matrix (same columns as scan)
#   kinship  : LOCO kinship list
#   addcovar : additive covariates or NULL
#   map      : marker map
#   threshold, peakdrop, drop : passed to find_peaks (drop = support interval)
#   effects  : "blup" (scan1blup) or "coef" (scan1coef)
peaks_with_effects <- function(scan, probs, pheno, kinship, addcovar, map,
                               threshold, peakdrop, drop, effects = "blup") {
  pk <- find_peaks(scan, map, threshold = threshold, peakdrop = peakdrop,
                   drop = drop)
  if (is.null(pk) || nrow(pk) == 0) return(list())
  out <- vector("list", nrow(pk))
  for (i in seq_len(nrow(pk))) {
    chr <- as.character(pk$chr[i])
    trait <- as.character(pk$lodcolumn[i])
    marker <- names(map[[chr]])[which.min(abs(map[[chr]] - pk$pos[i]))]
    pr <- probs[, chr]
    pr[[chr]] <- pr[[chr]][, , marker, drop = FALSE]
    k <- if (is.null(kinship)) NULL else if (is.list(kinship)) kinship[[chr]] else kinship
    y <- pheno[, trait, drop = FALSE]
    eff <- if (effects == "blup") {
      scan1blup(pr, y, kinship = k, addcovar = addcovar)
    } else {
      scan1coef(pr, y, kinship = k, addcovar = addcovar)
    }
    # Allele (DO: A-H) or genotype (e.g. F2: SS, SB, BB) columns.
    alleles <- intersect(colnames(eff), dimnames(probs[[chr]])[[2]])
    coef <- as.numeric(eff[1, alleles])
    names(coef) <- alleles
    out[[i]] <- list(trait = trait, chr = chr, pos = pk$pos[i], lod = pk$lod[i],
                     ci_lo = pk$ci_lo[i], ci_hi = pk$ci_hi[i], marker = marker,
                     coef = as.list(coef))
  }
  out
}

# Write the LOD profile as a gzipped CSV: marker, chr, pos, one column per trait.
write_profile <- function(scan, map, path) {
  chr <- rep(names(map), vapply(map, length, integer(1)))
  pos <- unlist(map, use.names = FALSE)
  marker <- unlist(lapply(map, names), use.names = FALSE)
  lod <- scan[marker, , drop = FALSE]
  df <- data.frame(marker = marker, chr = chr, pos = pos, lod,
                   check.names = FALSE, stringsAsFactors = FALSE)
  con <- gzfile(path, "w")
  on.exit(close(con))
  write.csv(df, con, row.names = FALSE)
  invisible(path)
}
