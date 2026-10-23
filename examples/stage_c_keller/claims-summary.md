# Keller 2019: draft claims for confirmation

25 claims. Positions, LODs and founder effects are taken from Supplemental Table 1 (sha256 659b3128…d88e) unless marked "text".
Default tolerances apply to all: position ±5 Mb (or the claimed position inside our 1.5-LOD support interval), LOD ±1.0, and the peak must reach LOD 6.

| ID | Trait (paper label) | Chr | Mb | LOD | Founder pattern |
|---|---|---|---|---|---|
| K01–K06 | 3.3G; 3.3G\|ins/islet; 8.3G\|ins/islet; AA\|ins/islet; GLP1; GLP1\|ins/islet | 1 | 29.02 | 6.61, 7.06, 6.13, 7.42, 6.82, 7.35 | CAST highest (text) |
| K07 | AA | 1 | 33.82 | 6.94 | CAST highest |
| K08 | GLP1\|8.3G | 2 | 83.83 | 7.54 | — |
| K09 | KCl\|3.3G | 3 | 41.15 | 6.35 | — |
| K10–K18 | GLP1\|3.3G; 16.7G\|3.3G; 8.3G\|3.3G; AA\|3.3G; 16.7G; PA\|3.3G; 16.7G\|ins/islet; PA; PA\|ins/islet | 3 | 133.6–136.0 | 8.26, 7.36, 6.82, 6.73, 6.38, 6.32, 6.09, 6.06, 6.17 | NOD, WSB high; CAST, PWK low (text) |
| K19 | GLP1\|8.3G | 10 | 102.46 | 6.08 | — |
| K20 | GLP1\|8.3G | 14 | 78.90 | 7.07 | — |
| K21 | KCl\|3.3G | 16 | 28.38 | 6.60 | — |
| K22–K23 | 8.3G\|ins/islet; GLP1\|ins/islet | 19 | 4.98 | 6.31, 6.28 | — |
| K24 | Glucagon, KCl (text) | 19 | ~5 | 6.9 | PWK high, NZO low (text) |
| K25 | GLP1 (Hunk, text) | 16 | 90.7 | absent: stays below LOD 6 | — |

The paper's own effect values pass our founder-pattern check for every claim with a pattern.

## Points to note

1. **Zfp148.** The text says the Chr 16 ~32 Mb KCl locus (LOD 6.5 at N = 300) fell below LOD 6 at N = 500. But Supplemental Table 1 lists KCl | 3.3G on Chr 16 at 28.38 Mb with LOD 6.60. I kept the table row as K21 and left out an absence claim for Zfp148, because the two sources disagree. The report will list this as an ambiguity.
2. **Sample size.** MPD lists about 240 mice per secretion measure, while the paper mapped 479. If the public file really has about 240 mice, LODs will come back lower and several claims will fail. That would be a data-availability result, and the report will say so.
3. **Trait mapping (assumption, set in run.yaml, not in the claims).** "X | 3.3G" and "X | 8.3G" map to MPD fold-change columns, e.g. INS_GLU8p3_GLP1_fc_G8p3. "X | ins/islet" maps to percent of insulin content (INS_*_pct). Unlabelled traits map to raw secretion. All are log-transformed, as the paper states. MPD's description for one measure (Attie2:115) disagrees with its variable name; I go by the variable name.
4. **Near-threshold peaks.** Nine claims have LOD below 6.4, so a small drop below LOD 6 makes them "not reproduced". That outcome is expected and is not evidence of anything wrong in the paper.
5. **Left out.** The count of 60 QTL above LOD 6 (needs every trait in the table mapped), the N = 300 interim scan, and in vivo traits.
