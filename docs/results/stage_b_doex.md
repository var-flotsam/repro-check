# Reproduction report: Broman KW. R/qtl2 user guide, DOex example (kbroman.org/qtl2, gh-pages f39901f3)

- DOI: none (R/qtl2 user guide)
- Run: `stage_b_doex`
- Claims frozen by Ethan (decision card, 2026-10-23T01:41Z) at 2026-10-23T01:42:18Z, sha256 `466aa85e8709ea23fc6cc1e4618529679abaa7ad5baf85c017c549d326a96260`
- Result: 1 reproduced

Verdicts are computed by `repro_check.compare` against tolerances fixed before the run. "Not reproduced" means the number fell outside the stated tolerance in this rerun; it says nothing about why.

## Results

| Claim | What the paper reports | Observed | Verdict |
|---|---|---|---|
| D1 | OF_immobile_pct: QTL at chr 2 ~96.8 Mb | chr 2 96.8422 Mb, LOD 10.97 | **reproduced** |

## Claim details

### D1: reproduced

- Source: user guide, 'There's a strong peak on chromosome 2' and peak_Mbp <- max(out, DOex$pmap)$pos
- Quote: "The marker is at 96.8 Mbp."
- Trait: `OF_immobile_pct` (N = 261)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 2 96.8 Mb | chr 2 96.8422 Mb (support 91.6018–103.878) | ±0.05 Mb | yes |
| threshold | LOD ≥ 6 | 10.97 | paper's threshold | yes |

Notes: Printed rounded to 0.1 Mb; threshold 6 is our reading of 'strong peak' (see ambiguities).

## Assumptions

1. {'Same steps as the user guide': 'calc_genoprob(error_prob=0.002) on gmap, genoprob_to_alleleprob, LOCO kinship from allele probabilities, sex as additive covariate.'}
2. Peak position reported on the physical map (pmap, Mb) at the same markers, as the guide's max(out, DOex$pmap).
3. Founder effects with scan1coef, as in the guide.
4. Covariates: Sex
5. Kinship: loco
6. Allele effects: scan1coef
7. Support interval: 1.5-LOD drop

## Inputs

| Input | Source | Retrieved | Bytes | sha256 |
|---|---|---|---|---|
| doex | https://raw.githubusercontent.com/rqtl/qtl2data/8cfeb3caa7fb1bec1fdfb5ad1e36015a17b1d17e/DOex/DOex.zip | 2026-10-23T01:42:18Z | 39590 | `a2a29481aa7010e08233ccb2925ae0e1806f2e8d98fbf1aeb244c33f3878d4af` |

## Environment

- Engine: qtl2, R version 4.4.3 (2025-02-28), qtl2 0.46
- repro-check 0.1.0, Python 3.13.16
- Seed: 20261023; permutations: 0
- Samples: 261; markers: 322
- Full R session info: `engine/session_info.txt`

## Ambiguities

- The guide says the chr 2 locus is "mostly due to the NZO allele" but not in which direction, so no founder claim is checked.
- The guide gives no LOD for the chr 2 peak. The claim uses LOD 6 as the bar for a "strong peak"; that number is ours.
