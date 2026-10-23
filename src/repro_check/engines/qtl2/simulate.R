# Synthetic Diversity Outbred-like data with planted QTL (Stage A).
#
#   Rscript simulate.R SPEC.json OUT_DIR
#
# Writes genoprobs.rds, map.rds, pheno.csv (id, sex, wave, traits, counts)
# and truth.json (where each QTL was planted). Everything is driven by
# spec[["seed"]] so the same spec gives byte-identical inputs.
#
# Model: each mouse carries two haplotypes per chromosome, each a mosaic of
# the 8 founders with crossovers at rate spec[["crossovers_per_100mb"]]. Allele
# probabilities are the haplotype dosages / 2, blurred by spec[["prob_noise"]] to
# mimic HMM uncertainty. A trait is
#   y = sum_f beta_f * dosage_f(marker) + sex effect + wave effect + noise
# and an expression gene is negative binomial with log mean shifted by the
# same dosage term (a local eQTL).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: Rscript simulate.R SPEC.json OUT_DIR")
script_dir <- dirname(normalizePath(sub("^--file=", "",
  grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(script_dir, "lib.R"))
suppressPackageStartupMessages(library(jsonlite))

spec <- fromJSON(args[1], simplifyVector = TRUE, simplifyDataFrame = FALSE)
out_dir <- args[2]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
set.seed(spec[["seed"]])

n <- spec[["n"]]
chr_len <- spec[["chr_length_mb"]]
spacing <- spec[["marker_spacing_mb"]]
chrs <- as.character(seq_len(spec[["n_chr"]]))
ids <- sprintf("SIM%04d", seq_len(n))
letters8 <- names(FOUNDERS)

map <- lapply(chrs, function(chr) {
  pos <- seq(spacing, chr_len, by = spacing)
  names(pos) <- sprintf("c%s_m%04d", chr, seq_along(pos))
  pos
})
names(map) <- chrs

# One haplotype: founder index at each marker position.
sim_haplotype <- function(pos) {
  n_x <- rpois(1, spec[["crossovers_per_100mb"]] * chr_len / 100)
  breaks <- sort(runif(n_x, 0, chr_len))
  seg_founders <- sample(8, n_x + 1, replace = TRUE)
  seg_founders[findInterval(pos, breaks) + 1]
}

probs <- lapply(chrs, function(chr) {
  pos <- map[[chr]]
  arr <- array(0, dim = c(n, 8, length(pos)),
               dimnames = list(ids, letters8, names(pos)))
  for (i in seq_len(n)) {
    h1 <- sim_haplotype(pos)
    h2 <- sim_haplotype(pos)
    for (j in seq_along(pos)) {
      arr[i, h1[j], j] <- arr[i, h1[j], j] + 0.5
      arr[i, h2[j], j] <- arr[i, h2[j], j] + 0.5
    }
  }
  if (spec[["prob_noise"]] > 0) {
    arr <- arr * (1 - spec[["prob_noise"]]) + spec[["prob_noise"]] / 8
  }
  arr
})
names(probs) <- chrs
attr(probs, "crosstype") <- "do"
attr(probs, "is_x_chr") <- setNames(rep(FALSE, length(chrs)), chrs)
attr(probs, "alleles") <- letters8
attr(probs, "alleleprobs") <- TRUE
class(probs) <- c("calc_genoprob", "list")

sex <- sample(c("F", "M"), n, replace = TRUE)
wave <- rep_len(seq_len(spec[["n_waves"]]), n)
pheno <- data.frame(id = ids, sex = sex, wave = wave, stringsAsFactors = FALSE)

nearest_marker <- function(chr, pos_mb) {
  chr <- as.character(chr)
  names(map[[chr]])[which.min(abs(map[[chr]] - pos_mb))]
}
dosage_term <- function(q) {
  m <- nearest_marker(q[["chr"]], q[["pos_mb"]])
  beta <- unlist(q[["founder_effects"]])[letters8]
  beta[is.na(beta)] <- 0
  as.numeric(probs[[as.character(q[["chr"]])]][, , m] %*% beta)
}

truth <- list(traits = list(), genes = list())
for (tr in spec[["traits"]]) {
  y <- rnorm(n, sd = tr[["noise_sd"]])
  y <- y + ifelse(sex == "M", spec[["sex_effect"]], 0) + spec[["wave_effect"]] * (wave - 1)
  for (q in tr[["qtl"]] %||% list()) y <- y + dosage_term(q)
  if (isTRUE(tr[["positive"]])) y <- exp(y / tr[["positive_scale"]])
  pheno[[tr[["name"]]]] <- y
  truth$traits[[tr[["name"]]]] <- list(qtl = tr[["qtl"]] %||% list(), positive = isTRUE(tr[["positive"]]))
}
for (g in spec[["genes"]] %||% list()) {
  libsize <- exp(rnorm(n, log(spec[["library_size"]]), 0.2))
  eta <- log(g[["base_rate"]]) + Reduce(`+`, lapply(g[["qtl"]] %||% list(), dosage_term), 0)
  pheno[[g[["name"]]]] <- rnbinom(n, size = g[["nb_size"]], mu = libsize * exp(eta))
  truth$genes[[g[["name"]]]] <- list(qtl = g[["qtl"]] %||% list())
}

saveRDS(probs, file.path(out_dir, "genoprobs.rds"))
saveRDS(map, file.path(out_dir, "map.rds"))
write.csv(pheno, file.path(out_dir, "pheno.csv"), row.names = FALSE)
writeLines(toJSON(list(spec = spec, truth = truth), auto_unbox = TRUE, pretty = TRUE,
                  digits = NA), file.path(out_dir, "truth.json"))
cat(sprintf("simulated %d mice, %d chromosomes, %d markers\n", n, length(chrs),
            sum(vapply(map, length, integer(1)))))
