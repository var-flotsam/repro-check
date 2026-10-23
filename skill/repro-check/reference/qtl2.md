# R/qtl2 engine notes

## Contents
- What the engine does
- Defaults and when to record an assumption
- Diversity Outbred specifics

## What the engine does

`engine.R` reads genotype probabilities (`calc_genoprob` or allele
probabilities, saved as .rds), a marker map (.rds list of named positions in
Mb), and CSV phenotypes and covariates. It runs `scan1` with a kinship random
effect, calls peaks with `find_peaks`, and estimates founder effects at each
peak. It writes `results.json`, `lod_profile.csv.gz` and `session_info.txt`.

## Defaults and when to record an assumption

| Setting | Default | Record as an assumption when |
|---|---|---|
| `kinship` | `loco` | the paper doesn't say LOCO |
| `addcovar` | none | the paper names covariates without saying how they were coded |
| `covar_factors` | none | a batch or wave covariate is treated as a factor |
| `transform` | `none` | the paper's transform is unclear (log, rank-Z, log1p for counts) |
| `effects` | `blup` | the paper doesn't say BLUP or fixed coefficients |
| `ci_drop` | 1.5 | the paper uses another support interval or Bayes interval |
| `peakdrop` | 1.5 | two peaks on one chromosome need separating |
| `report_threshold` | 3 | must be at or below every claim's `threshold_lod` |
| `n_perm` | 0 | the paper's thresholds come from permutations you want to check |

Also record: which genotype probability release was used, genome build, and
how many samples were dropped for missing data (`n_mapped` per trait).

## Diversity Outbred specifics

- Eight founders A–H; allele probabilities are 8 columns.
- Mapping uses the additive allele model (`scan1` on allele probabilities).
- Sex and generation or wave are the usual additive covariates.
- Peak positions shift by a few Mb between genotype probability releases and
  marker sets, so position tolerances under ~2 Mb are rarely fair.
