# Stage C preparation: turn the MPD Attie2 animal data and lesson covariates
# into the engine's pheno.csv and covar.csv, by the columns in TRAIT_MAP.csv.
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

# MPD's "csvanimaldata" export is wide: one row per mouse, one column per
# measure, named by MPD variable name (trait_map.csv: mpd_column).
mpd <- read.csv(inp("mpd"), stringsAsFactors = FALSE, check.names = FALSE)
if (!"animal_id" %in% colnames(mpd))
  stop("MPD file has no 'animal_id' column; columns are: ", paste(colnames(mpd), collapse = ", "))
missing_cols <- setdiff(tmap$mpd_column, colnames(mpd))
if (length(missing_cols)) stop("MPD file lacks column(s): ", paste(missing_cols, collapse = ", "))
if (anyDuplicated(mpd$animal_id)) stop("MPD file has duplicated animal_id values")

covar <- readRDS(inp("covar"))
covar <- as.data.frame(covar, stringsAsFactors = FALSE)
if (!"mouse" %in% colnames(covar)) stop("covariates have no 'mouse' column")

ids <- as.character(mpd$animal_id)
overlap <- intersect(ids, as.character(covar$mouse))
if (length(overlap) < 0.5 * length(ids))
  stop(sprintf("only %d of %d MPD animal IDs match covariate IDs (e.g. MPD '%s' vs covar '%s')",
               length(overlap), length(ids), ids[1], covar$mouse[1]))

pheno <- data.frame(id = overlap, stringsAsFactors = FALSE)
rows <- match(overlap, ids)
for (i in seq_len(nrow(tmap))) {
  pheno[[tmap$trait[i]]] <- suppressWarnings(as.numeric(mpd[[tmap$mpd_column[i]]][rows]))
}
cv <- covar[match(overlap, as.character(covar$mouse)), c("mouse", "sex", "DOwave")]
colnames(cv)[1] <- "id"
write.csv(pheno, file.path(out, "pheno.csv"), row.names = FALSE)
write.csv(cv, file.path(out, "covar.csv"), row.names = FALSE)

mp <- readRDS(inp("map"))
log <- list(
  mpd_columns = as.list(setNames(tmap$mpd_column, tmap$trait)),
  mpd_animals = length(ids), matched_to_covariates = length(overlap),
  n_per_trait = as.list(colSums(!is.na(pheno[, -1, drop = FALSE]))),
  map_chr1_max_pos = max(mp[["1"]]), map_n_markers = sum(lengths(mp))
)
writeLines(toJSON(log, auto_unbox = TRUE, pretty = TRUE), file.path(out, "prepare_log.json"))
cat(toJSON(log, auto_unbox = TRUE, pretty = TRUE), "\n")
