# Redraw a paper's figures from this run's engine output.
#
#   Rscript figures.R FIGURES_SPEC.json
#
# Reads ENGINE_DIR/{lod_profile.csv.gz, results.json, effects_<id>.csv} and
# writes OUT_DIR/<id>.png, <id>.pdf, <id>.csv (the numbers drawn) and
# index.json. Nothing here compares with the paper: figures get no verdict.

suppressPackageStartupMessages(library(jsonlite))
`%||%` <- function(a, b) if (is.null(a) || length(a) == 0) b else a

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: Rscript figures.R FIGURES_SPEC.json")
spec <- fromJSON(args[1], simplifyVector = TRUE, simplifyDataFrame = FALSE)
eng <- spec[["engine_dir"]]
out <- spec[["out_dir"]]
units <- spec[["units"]] %||% "Mb"
dir.create(out, showWarnings = FALSE, recursive = TRUE)

prof <- read.csv(gzfile(file.path(eng, "lod_profile.csv.gz")), check.names = FALSE,
                 stringsAsFactors = FALSE, colClasses = c(chr = "character"))
res <- fromJSON(file.path(eng, "results.json"), simplifyVector = TRUE, simplifyDataFrame = FALSE)
peaks <- res[["peaks"]] %||% list()

# Collaborative Cross founder colours (as qtl2::CCcolors).
CC <- c(A = "#F0F000", B = "#808080", C = "#F08080", D = "#1010F0",
        E = "#00A0F0", F = "#00A000", G = "#F00000", H = "#9000E0")
CC_NAMES <- c(A = "AJ", B = "B6", C = "129", D = "NOD", E = "NZO", F = "CAST", G = "PWK", H = "WSB")
TRAIT_COLS <- c("#1f4e79", "#c0504d", "#4f8f3a", "#7f5fa8", "#d08a1e", "#2a9d8f")

chr_order <- unique(prof$chr)
need_traits <- function(traits) {
  miss <- setdiff(traits, colnames(prof))
  if (length(miss)) stop("trait(s) not in this run: ", paste(miss, collapse = ", "))
}
thresholds <- function(fig) unlist(fig[["thresholds"]]) %||% spec[["default_threshold"]]

# Cumulative genome positions with a gap between chromosomes.
genome_x <- function() {
  len <- tapply(prof$pos, factor(prof$chr, levels = chr_order), max)
  start <- tapply(prof$pos, factor(prof$chr, levels = chr_order), min)
  gap <- 0.01 * sum(len - start)
  off <- c(0, cumsum(len - start + gap))[seq_along(chr_order)]
  names(off) <- chr_order
  list(x = prof$pos - start[prof$chr] + off[prof$chr], off = off, start = start, len = len)
}

draw <- function(id, fn, width = 9, height = 4.5) {
  png(file.path(out, paste0(id, ".png")), width = width, height = height, units = "in", res = 150)
  fn(); dev.off()
  pdf(file.path(out, paste0(id, ".pdf")), width = width, height = height)
  fn(); dev.off()
}

caption <- function(fig) mtext(sprintf("%s: %s (regenerated from this run; no verdict)", fig[["id"]], fig[["source"]]),
                              side = 3, line = 0.3, adj = 0, cex = 0.8)

fig_genome_scan <- function(fig) {
  traits <- unlist(fig[["traits"]]); need_traits(traits)
  g <- genome_x()
  ymax <- max(c(unlist(prof[traits]), thresholds(fig)), na.rm = TRUE) * 1.05
  draw(fig[["id"]], function() {
    par(mar = c(4, 4, 2, 1))
    plot(NA, xlim = range(g$x), ylim = c(0, ymax), xaxt = "n", xlab = "Chromosome", ylab = "LOD",
         xaxs = "i", yaxs = "i", bty = "l")
    for (i in seq_along(chr_order)) if (i %% 2 == 0)
      rect(g$off[i], 0, g$off[i] + g$len[i] - g$start[i], ymax, col = "grey94", border = NA)
    axis(1, at = g$off + (g$len - g$start) / 2, labels = chr_order, tick = FALSE, cex.axis = 0.7)
    for (j in seq_along(traits)) for (ch in chr_order) {
      w <- prof$chr == ch
      lines(g$x[w], prof[[traits[j]]][w], col = TRAIT_COLS[(j - 1) %% length(TRAIT_COLS) + 1], lwd = 1)
    }
    abline(h = thresholds(fig), lty = 2, col = "grey40")
    if (length(traits) > 1) legend("topright", traits, col = TRAIT_COLS[seq_along(traits)], lwd = 2,
                                   bty = "n", cex = 0.7)
    caption(fig)
  })
  prof[, c("marker", "chr", "pos", traits)]
}

fig_lod_chr <- function(fig) {
  traits <- unlist(fig[["traits"]]); need_traits(traits)
  ch <- fig[["chr"]]
  w <- prof$chr == ch
  reg <- unlist(fig[["region"]])
  if (!is.null(reg)) w <- w & prof$pos >= reg[1] & prof$pos <= reg[2]
  if (!any(w)) stop(sprintf("figure %s: no markers on chr %s in range", fig[["id"]], ch))
  d <- prof[w, c("marker", "chr", "pos", traits)]
  ymax <- max(c(unlist(d[traits]), thresholds(fig)), na.rm = TRUE) * 1.05
  draw(fig[["id"]], function() {
    par(mar = c(4, 4, 2, 1))
    plot(NA, xlim = range(d$pos), ylim = c(0, ymax), xlab = sprintf("Chr %s position (%s)", ch, units),
         ylab = "LOD", yaxs = "i", bty = "l")
    for (p in peaks) if (p$chr == ch && p$trait %in% traits)
      rect(p$ci_lo, 0, p$ci_hi, ymax, col = adjustcolor("grey70", 0.35), border = NA)
    for (j in seq_along(traits)) lines(d$pos, d[[traits[j]]], col = TRAIT_COLS[(j - 1) %% length(TRAIT_COLS) + 1], lwd = 1.5)
    abline(h = thresholds(fig), lty = 2, col = "grey40")
    if (length(traits) > 1) legend("topright", traits, col = TRAIT_COLS[seq_along(traits)], lwd = 2,
                                   bty = "n", cex = 0.7)
    caption(fig)
  })
  d
}

fig_allele_effects <- function(fig) {
  trait <- unlist(fig[["traits"]])[1]; need_traits(trait)
  path <- file.path(eng, sprintf("effects_%s.csv", fig[["id"]]))
  if (!file.exists(path)) stop(sprintf("figure %s: %s missing; run the engine with the frozen claims (repro-check run --claims)",
                                       fig[["id"]], basename(path)))
  eff <- read.csv(path, check.names = FALSE, stringsAsFactors = FALSE)
  alleles <- setdiff(colnames(eff), c("marker", "pos"))
  cols <- if (all(alleles %in% names(CC))) CC[alleles] else TRAIT_COLS[seq_along(alleles)]
  labs <- if (all(alleles %in% names(CC))) CC_NAMES[alleles] else alleles
  ch <- fig[["chr"]]
  w <- prof$chr == ch & prof$pos >= min(eff$pos) & prof$pos <= max(eff$pos)
  d <- prof[w, c("pos", trait)]
  draw(fig[["id"]], function() {
    layout(matrix(1:2, ncol = 1), heights = c(3, 2))
    par(mar = c(0.5, 4, 2, 6), xpd = FALSE)
    plot(NA, xlim = range(eff$pos), ylim = range(unlist(eff[alleles]), na.rm = TRUE), xaxt = "n",
         xlab = "", ylab = "Founder effect", bty = "l")
    for (a in seq_along(alleles)) lines(eff$pos, eff[[alleles[a]]], col = cols[a], lwd = 2)
    abline(h = 0, col = "grey70")
    par(xpd = TRUE)
    legend(par("usr")[2], par("usr")[4], labs, col = cols, lwd = 2, bty = "n", cex = 0.75)
    par(xpd = FALSE)
    caption(fig)
    par(mar = c(4, 4, 0.5, 6))
    plot(d$pos, d[[trait]], type = "l", xlim = range(eff$pos), xlab = sprintf("Chr %s position (%s)", ch, units),
         ylab = "LOD", bty = "l", lwd = 1.5)
    abline(h = thresholds(fig), lty = 2, col = "grey40")
  }, height = 6)
  eff
}

fig_peak_map <- function(fig) {
  traits <- unlist(fig[["traits"]]) %||% unique(vapply(peaks, function(p) p$trait, ""))
  thr <- min(thresholds(fig))
  ps <- Filter(function(p) p$trait %in% traits && p$lod >= thr, peaks)
  d <- if (length(ps)) do.call(rbind, lapply(ps, function(p)
    data.frame(trait = p$trait, chr = p$chr, pos = p$pos, lod = p$lod, stringsAsFactors = FALSE))) else
    data.frame(trait = character(), chr = character(), pos = numeric(), lod = numeric())
  g <- genome_x()
  start <- g$start; off <- g$off
  d$x <- if (nrow(d)) d$pos - start[d$chr] + off[d$chr] else numeric()
  draw(fig[["id"]], function() {
    par(mar = c(4, 10, 2, 1))
    plot(NA, xlim = range(g$x), ylim = c(0.5, length(traits) + 0.5), xaxt = "n", yaxt = "n",
         xlab = "Chromosome", ylab = "", xaxs = "i", bty = "l")
    for (i in seq_along(chr_order)) if (i %% 2 == 0)
      rect(off[i], 0, off[i] + g$len[i] - start[i], length(traits) + 1, col = "grey94", border = NA)
    axis(1, at = off + (g$len - start) / 2, labels = chr_order, tick = FALSE, cex.axis = 0.7)
    axis(2, at = seq_along(traits), labels = traits, las = 1, cex.axis = 0.6)
    if (nrow(d)) points(d$x, match(d$trait, traits), pch = 19, cex = pmin(3, 0.6 + 0.2 * (d$lod - thr)),
                        col = adjustcolor("#c0504d", 0.8))
    caption(fig)
  }, height = max(3, 1 + 0.25 * length(traits)))
  d[, c("trait", "chr", "pos", "lod")]
}

index <- list()
for (fig in spec[["figures"]]) {
  data <- switch(fig[["kind"]],
    genome_scan = fig_genome_scan(fig), lod_chr = fig_lod_chr(fig),
    allele_effects = fig_allele_effects(fig), peak_map = fig_peak_map(fig),
    stop("unknown figure kind ", fig[["kind"]]))
  write.csv(data, file.path(out, paste0(fig[["id"]], ".csv")), row.names = FALSE)
  index[[length(index) + 1]] <- list(id = fig[["id"]], kind = fig[["kind"]], source = fig[["source"]],
                                     url = fig[["url"]] %||% "", png = paste0(fig[["id"]], ".png"),
                                     pdf = paste0(fig[["id"]], ".pdf"), data = paste0(fig[["id"]], ".csv"))
  cat(sprintf("drew %s (%s)\n", fig[["id"]], fig[["kind"]]))
}
writeLines(toJSON(index, auto_unbox = TRUE, pretty = TRUE), file.path(out, "index.json"))
