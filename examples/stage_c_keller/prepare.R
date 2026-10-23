# Stage C preparation: turn the MPD Attie2 animal data and lesson covariates
# into the engine's pheno.csv and covar.csv, by MPD measure number only.
#
#   Rscript prepare.R RUN_DIR TRAIT_MAP.csv
#
# Stops, rather than guessing, if IDs or columns don't line up. Writes
# RUN_DIR/derived/{pheno.csv, covar.csv, prepare_log.json}.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: Rscript prepare.R RUN_DIR TRAIT_MAP.csv")
suppressPackageStartupMessages(library(jsonlite))
run <- args[1]
prov <- fromJSON(file.path(run, "provenance.json"))
inp <- function(n) file.path(run, prov$inputs[[n]]$path)
out <- file.path(run, "derived"); dir.create(out, showWarnings = FALSE)
tmap <- read.csv(args[2], stringsAsFactors = FALSE, check.names = FALSE)

mpd <- read.csv(inp("mpd"), stringsAsFactors = FALSE, check.names = FALSE)
cn <- tolower(colnames(mpd))
pick <- function(cands) {
  hit <- match(cands, cn); hit <- hit[!is.na(hit)]
  if (length(hit) == 0) stop("MPD file has none of the columns: ", paste(cands, collapse = ", "),
                             "; columns are: ", paste(colnames(mpd), collapse = ", "))
  colnames(mpd)[hit[1]]
}
c_id <- pick(c("animal_id", "animalid", "subjectid", "subject_id", "mouse_id", "id"))
c_meas <- pick(c("measnum", "measure_id", "measureid"))
c_val <- pick(c("value", "measval", "val"))

covar <- readRDS(inp("covar"))
covar <- as.data.frame(covar, stringsAsFactors = FALSE)
if (!"mouse" %in% colnames(covar)) stop("covariates have no 'mouse' column")
probs_ids <- NULL  # checked by the engine; here we only compare MPD with covariates

missing_meas <- setdiff(tmap$mpd_measnum, unique(mpd[[c_meas]]))
if (length(missing_meas)) stop("MPD file lacks measure(s): ", paste(missing_meas, collapse = ", "))

ids <- sort(unique(as.character(mpd[[c_id]])))
overlap <- intersect(ids, as.character(covar$mouse))
if (length(overlap) < 0.5 * length(ids))
  stop(sprintf("only %d of %d MPD animal IDs match covariate IDs (e.g. MPD '%s' vs covar '%s')",
               length(overlap), length(ids), ids[1], covar$mouse[1]))

pheno <- data.frame(id = overlap, stringsAsFactors = FALSE)
dups <- list()
for (i in seq_len(nrow(tmap))) {
  sub <- mpd[mpd[[c_meas]] == tmap$mpd_measnum[i], ]
  n_dup <- sum(duplicated(sub[[c_id]]))
  if (n_dup > 0) stop(sprintf("measure %s has %d duplicated animal IDs", tmap$mpd_measnum[i], n_dup))
  pheno[[tmap$trait[i]]] <- as.numeric(sub[[c_val]][match(pheno$id, as.character(sub[[c_id]]))])
}
cv <- covar[match(overlap, as.character(covar$mouse)), c("mouse", "sex", "DOwave")]
colnames(cv)[1] <- "id"
write.csv(pheno, file.path(out, "pheno.csv"), row.names = FALSE)
write.csv(cv, file.path(out, "covar.csv"), row.names = FALSE)

mp <- readRDS(inp("map"))
log <- list(
  mpd_columns = list(id = c_id, measnum = c_meas, value = c_val),
  mpd_animals = length(ids), matched_to_covariates = length(overlap),
  n_per_trait = as.list(colSums(!is.na(pheno[, -1, drop = FALSE]))),
  map_chr1_max_pos = max(mp[["1"]]), map_n_markers = sum(lengths(mp))
)
writeLines(toJSON(log, auto_unbox = TRUE, pretty = TRUE), file.path(out, "prepare_log.json"))
cat(toJSON(log, auto_unbox = TRUE, pretty = TRUE), "\n")
