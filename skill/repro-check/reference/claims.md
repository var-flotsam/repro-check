# Claims file reference

## Contents
- Layout
- Claim kinds
- Tolerances and their defaults
- How verdicts are decided

## Layout

```yaml
paper:
  doi: 10.1172/JCI129143
  citation: Keller MP et al. J Clin Invest 2019;129(10):4419-4432
claims:
  - id: C1
    kind: qtl_peak
    source: "Results, Fig 3A"
    quote: "a QTL ... at ~34 Mb"
    trait: ins_8p3_glp1          # trait name as given in run.yaml
    chr: "1"
    pos_mb: 34
    pos_reported_precision_mb: 1 # the paper printed "~34"
    lod: null                    # leave null if the paper gives no number
    founders_high: [CAST]        # names or letters A-H
    founders_low: []
    tolerance: {pos_mb: 5}       # only the keys you want to override
    notes: ""
```

`paper.position_units` is `Mb` (default) or `cM`; `pos_mb` and the
`pos_mb` tolerance are then read in those units.

`freeze` adds a `frozen:` block (who, when, sha256). Do not write it by hand.

Founders: A AJ, B B6, C 129, D NOD, E NZO, F CAST, G PWK, H WSB.

## Claim kinds

| kind | Needs | Reproduced when |
|---|---|---|
| `qtl_peak` | trait, chr, pos_mb; optional lod, founders | a peak at or above `threshold_lod` lies within the position window, and the LOD and founder checks pass if given |
| `qtl_absent` | trait, chr, pos_mb | the highest LOD in the window stays below `threshold_lod` |
| `effect_pattern` | trait, chr, pos_mb, founders | a peak is found as for `qtl_peak` and the founder pattern matches |
| `count` | traits (list), value | peaks at or above `threshold_lod` across those traits is within `count_rel` of value |
| `perm_threshold` | trait, alpha, value | the engine's permutation threshold at that alpha is within `lod_abs` of value (needs `n_perm` and `perm_alpha` in run.yaml) |

## Tolerances and their defaults

| key | default | meaning |
|---|---|---|
| `pos_mb` | 5.0 | window half-width; the larger of this and `pos_reported_precision_mb` is used. A claimed position inside the observed support interval also passes |
| `pos_ci` | 1 | 1: a claimed position inside the observed support interval also passes; 0: distance only (use 0 for the authors' own data and software) |
| `lod_abs` | 1.0 | allowed LOD difference |
| `lod_rel`, `lod_rel_above` | 0.15, 10 | for claimed LOD above 10, allow 15% instead |
| `threshold_lod` | 6.0 | the paper's threshold; set it to what the paper used |
| `count_rel` | 0.20 | relative tolerance for counts |

Write the reason for any non-default tolerance in `notes`.

## How verdicts are decided

- **reproduced**: every check passes.
- **partly reproduced**: the peak is found (position and threshold pass) but
  the LOD or founder check fails.
- **not reproduced**: no peak above threshold in the window, or for
  `qtl_absent` a peak crosses the threshold.
- **not checkable**: the trait was not mapped, or the window has no markers.
  Never counted as reproduced.

A single listed founder must be the extreme (highest for `founders_high`,
lowest for `founders_low`). Several listed founders must all fall in that
half of the eight.

## Figures

Optional `figures:` list in the same file, frozen and hashed with the claims.
Figures are redrawn from the run; they never get a verdict.

```yaml
figures:
  - id: F3B
    kind: allele_effects     # genome_scan | lod_chr | allele_effects | peak_map
    source: Figure 3B        # the paper's figure and panel
    url: https://...         # optional link to the figure
    traits: [ins_AA]         # genome_scan, lod_chr: 1+; allele_effects: exactly 1; peak_map: optional (all)
    chr: "1"                 # lod_chr, allele_effects
    region: [20, 50]         # optional, in the paper's position units
    thresholds: [6]          # optional LOD lines (default: 6)
    notes: what the paper shows that this run cannot draw
```

A figure list written after a run is a separate figures-only file (`paper`
and `figures`, no `claims`), frozen on its own and passed with `--figures`.
Its `paper.notes` must say it was declared after the run.
