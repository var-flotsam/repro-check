# Reproduction report: Broman KW. R/qtl2 user guide, iron example (kbroman.org/qtl2, gh-pages f39901f3)

- DOI: none (R/qtl2 user guide)
- Run: `stage_b_iron`
- Claims frozen by Ethan (decision card, 2026-10-23T01:41Z) at 2026-10-23T01:41:31Z, sha256 `d21e7276243c81e8873386750b93b8a221074a2f6cb979af0b62ef87e149a535`
- Result: 10 reproduced, 1 not reproduced

Verdicts are computed by `repro_check.compare` against tolerances fixed before the run. "Not reproduced" means the number fell outside the stated tolerance in this rerun; it says nothing about why.

## Results

| Claim | What the paper reports | Observed | Verdict |
|---|---|---|---|
| B1 | liver: QTL at chr 2 ~56.8 cM, LOD 4.9576 | chr 2 56.8 cM, LOD 4.96 | **reproduced** |
| B2 | liver: QTL at chr 7 ~50.1 cM, LOD 4.0508 | chr 7 50.1 cM, LOD 4.05 | **reproduced** |
| B3 | liver: QTL at chr 16 ~28.6 cM, LOD 7.6816 | chr 16 28.6 cM, LOD 7.68 | **reproduced** |
| B4 | spleen: QTL at chr 8 ~13.6 cM, LOD 4.3029 | chr 8 13.6 cM, LOD 4.30 | **reproduced** |
| B5 | spleen: QTL at chr 9 ~56.6 cM, LOD 12.0632 | chr 9 56.6 cM, LOD 12.06 | **reproduced** |
| B6 | 3 QTL above LOD 4 | 3 | **reproduced** |
| B7 | 2 QTL above LOD 4 | 2 | **reproduced** |
| B8 | liver: LOD threshold 3.46 at alpha 0.05 | 3.30 | **not reproduced** |
| B9 | spleen: LOD threshold 3.46 at alpha 0.05 | 3.47 | **reproduced** |
| B10 | liver: LOD threshold 2.63 at alpha 0.2 | 2.65 | **reproduced** |
| B11 | spleen: LOD threshold 2.64 at alpha 0.2 | 2.64 | **reproduced** |

## Claim details

### B1: reproduced

- Source: user guide, find_peaks(out, map, threshold=4, drop=1.5)
- Quote: "liver 2 56.8 4.9576 48.1 73.2"
- Trait: `liver` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 2 56.8 cM | chr 2 56.8 cM (support 48.1–73.2) | ±1 cM | yes |
| threshold | LOD ≥ 4 | 4.96 | paper's threshold | yes |
| LOD | 4.96 | 4.96 (difference -0.00) | ±0.01 | yes |

### B2: reproduced

- Source: user guide, find_peaks table
- Quote: "liver 7 50.1 4.0508 13.1 53.6"
- Trait: `liver` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 7 50.1 cM | chr 7 50.1 cM (support 13.1–53.6) | ±1 cM | yes |
| threshold | LOD ≥ 4 | 4.05 | paper's threshold | yes |
| LOD | 4.05 | 4.05 (difference -0.00) | ±0.01 | yes |

### B3: reproduced

- Source: user guide, find_peaks table
- Quote: "liver 16 28.6 7.6816 6.6 40.4"
- Trait: `liver` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 16 28.6 cM | chr 16 28.6 cM (support 6.6–40.4) | ±1 cM | yes |
| threshold | LOD ≥ 4 | 7.68 | paper's threshold | yes |
| LOD | 7.68 | 7.68 (difference -0.00) | ±0.01 | yes |

### B4: reproduced

- Source: user guide, find_peaks table
- Quote: "spleen 8 13.6 4.3029 0.0 32.7"
- Trait: `spleen` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 8 13.6 cM | chr 8 13.6 cM (support 0–32.7) | ±1 cM | yes |
| threshold | LOD ≥ 4 | 4.30 | paper's threshold | yes |
| LOD | 4.30 | 4.30 (difference +0.00) | ±0.01 | yes |

### B5: reproduced

- Source: user guide, find_peaks table
- Quote: "spleen 9 56.6 12.0632 53.6 61.2"
- Trait: `spleen` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 9 56.6 cM | chr 9 56.6 cM (support 53.6–61.2) | ±1 cM | yes |
| threshold | LOD ≥ 4 | 12.06 | paper's threshold | yes |
| LOD | 12.06 | 12.06 (difference +0.00) | ±1.81 | yes |

### B6: reproduced

- Source: user guide, find_peaks table
- Quote: "three liver rows above LOD 4"

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| count | 3 | 3 | ±0% | yes |

### B7: reproduced

- Source: user guide, find_peaks table
- Quote: "two spleen rows above LOD 4"

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| count | 2 | 2 | ±0% | yes |

### B8: not reproduced

- Source: user guide, summary(operm, alpha=c(0.2, 0.05))
- Quote: "0.05 3.46 3.46"
- Trait: `liver` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| permutation threshold (alpha 0.05) | 3.46 | 3.30 (difference -0.16) | ±0.15 | no |

Notes: 1000 permutations; the Monte Carlo error of a 95th percentile is about 0.1 LOD

### B9: reproduced

- Source: user guide, summary(operm)
- Quote: "0.05 3.46 3.46"
- Trait: `spleen` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| permutation threshold (alpha 0.05) | 3.46 | 3.47 (difference +0.01) | ±0.15 | yes |

### B10: reproduced

- Source: user guide, summary(operm, alpha=c(0.2, 0.05))
- Quote: "0.2 2.63 2.64"
- Trait: `liver` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| permutation threshold (alpha 0.2) | 2.63 | 2.65 (difference +0.02) | ±0.15 | yes |

### B11: reproduced

- Source: user guide, summary(operm, alpha=c(0.2, 0.05))
- Quote: "0.2 2.63 2.64"
- Trait: `spleen` (N = 284)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| permutation threshold (alpha 0.2) | 2.64 | 2.64 (difference +0.00) | ±0.15 | yes |

## Assumptions

1. {'Same steps as the user guide': 'insert_pseudomarkers(gmap, step=1), calc_genoprob(error_prob=0.002), scan1 with Xcovar and no kinship.'}
2. find_peaks with peakdrop=Inf (the guide's first table) and drop=1.5.
3. Permutations use our seed, not the guide's (it sets none), so thresholds can differ by Monte Carlo error.
4. Covariates: none
5. Kinship: none
6. Allele effects: scan1coef
7. Support interval: 1.5-LOD drop

## Inputs

| Input | Source | Retrieved | Bytes | sha256 |
|---|---|---|---|---|
| iron | https://raw.githubusercontent.com/kbroman/qtl2/3329fb52cdced4762c6f82b3b5e3c294382ad9ca/inst/extdata/iron.zip | 2026-10-23T01:41:31Z | 11670 | `125d037dca211459946114891b8c2d98f71aa6925ebfb1472e9b46a88c3623b6` |

## Environment

- Engine: qtl2, R version 4.4.3 (2025-02-28), qtl2 0.46
- repro-check 0.1.0, Python 3.13.16
- Seed: 20261023; permutations: 1000
- Samples: 284; markers: 881
- Full R session info: `engine/session_info.txt`

## Ambiguities

- The user guide was rendered with an earlier qtl2 release than 0.46; small numeric differences are possible.
