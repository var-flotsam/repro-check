# Reproduction report: Keller MP et al. Gene loci associated with insulin secretion in islets from nondiabetic mice. J Clin Invest 2019;129(10):4419-4432

- DOI: 10.1172/JCI129143
- Run: `stage_c_keller`
- Claims frozen by Ethan (decision card, 2026-10-23T03:36Z) at 2026-10-23T03:38:26Z, sha256 `20bfae0e35fc71f983828ce7a7abe33349d3581922e6b10bcbbb89660c13715a`
- Result: 11 reproduced, 2 partly reproduced, 12 not reproduced

Verdicts are computed by `repro_check.compare` against tolerances fixed before the run. "Not reproduced" means the number fell outside the stated tolerance in this rerun; it says nothing about why.

## Results

| Claim | What the paper reports | Observed | Verdict |
|---|---|---|---|
| K01 | ins_3.3G: QTL at chr 1 ~29.0228 Mb, LOD 6.6069, CAST high | chr 1 51.8047 Mb, LOD 6.44 | **partly reproduced** |
| K02 | ins_3.3G_per_content: QTL at chr 1 ~29.0228 Mb, LOD 7.0644, CAST high | chr 1 29.0228 Mb, LOD 6.21 | **reproduced** |
| K03 | ins_8.3G_per_content: QTL at chr 1 ~29.0228 Mb, LOD 6.1346, CAST high | chr 1 29.0228 Mb, LOD 5.87 | **not reproduced** |
| K04 | ins_AA_per_content: QTL at chr 1 ~29.0228 Mb, LOD 7.4243, CAST high | chr 1 29.0228 Mb, LOD 7.76 | **reproduced** |
| K05 | ins_GLP1: QTL at chr 1 ~29.0228 Mb, LOD 6.8223, CAST high | chr 1 29.0228 Mb, LOD 6.62 | **reproduced** |
| K06 | ins_GLP1_per_content: QTL at chr 1 ~29.0228 Mb, LOD 7.3471, CAST high | chr 1 29.0228 Mb, LOD 7.40 | **reproduced** |
| K07 | ins_AA: QTL at chr 1 ~33.8178 Mb, LOD 6.9389, CAST high | chr 1 33.8178 Mb, LOD 7.07 | **reproduced** |
| K08 | ins_GLP1_fc_8.3G: QTL at chr 2 ~83.826 Mb, LOD 7.5381 | chr 2 91.4305 Mb, LOD 6.39 | **partly reproduced** |
| K09 | ins_KCl_fc_3.3G: QTL at chr 3 ~41.1508 Mb, LOD 6.3472 | chr 3 70.0835 Mb, LOD 5.05 | **not reproduced** |
| K10 | ins_GLP1_fc_3.3G: QTL at chr 3 ~135.518 Mb, LOD 8.2587, NOD, WSB high, CAST, PWK low | chr 3 135.518 Mb, LOD 7.41 | **reproduced** |
| K11 | ins_16.7G_fc_3.3G: QTL at chr 3 ~135.518 Mb, LOD 7.3566, NOD, WSB high, CAST, PWK low | max LOD 4.83 at 135.518 Mb | **not reproduced** |
| K12 | ins_8.3G_fc_3.3G: QTL at chr 3 ~135.233 Mb, LOD 6.8219, NOD, WSB high, CAST, PWK low | chr 3 135.72 Mb, LOD 6.23 | **reproduced** |
| K13 | ins_AA_fc_3.3G: QTL at chr 3 ~136.023 Mb, LOD 6.727, NOD, WSB high, CAST, PWK low | chr 3 136.023 Mb, LOD 6.90 | **reproduced** |
| K14 | ins_16.7G: QTL at chr 3 ~135.518 Mb, LOD 6.3817, NOD, WSB high, CAST, PWK low | chr 3 133.553 Mb, LOD 5.86 | **not reproduced** |
| K15 | ins_PA_fc_3.3G: QTL at chr 3 ~135.518 Mb, LOD 6.3163, NOD, WSB high, CAST, PWK low | max LOD 3.47 at 135.518 Mb | **not reproduced** |
| K16 | ins_16.7G_per_content: QTL at chr 3 ~133.561 Mb, LOD 6.0938, NOD, WSB high, CAST, PWK low | chr 3 133.651 Mb, LOD 5.77 | **not reproduced** |
| K17 | ins_PA: QTL at chr 3 ~133.651 Mb, LOD 6.0569, NOD, WSB high, CAST, PWK low | chr 3 133.651 Mb, LOD 5.64 | **not reproduced** |
| K18 | ins_PA_per_content: QTL at chr 3 ~133.651 Mb, LOD 6.1669, NOD, WSB high, CAST, PWK low | chr 3 133.651 Mb, LOD 5.52 | **not reproduced** |
| K19 | ins_GLP1_fc_8.3G: QTL at chr 10 ~102.456 Mb, LOD 6.0849 | chr 10 98.9982 Mb, LOD 5.22 | **not reproduced** |
| K20 | ins_GLP1_fc_8.3G: QTL at chr 14 ~78.899 Mb, LOD 7.0659 | chr 14 79.2106 Mb, LOD 5.97 | **not reproduced** |
| K21 | ins_KCl_fc_3.3G: QTL at chr 16 ~28.3788 Mb, LOD 6.5976 | max LOD 3.94 at 24.1548 Mb | **not reproduced** |
| K22 | ins_8.3G_per_content: QTL at chr 19 ~4.9781 Mb, LOD 6.3145 | chr 19 4.97811 Mb, LOD 6.26 | **reproduced** |
| K23 | ins_GLP1_per_content: QTL at chr 19 ~4.9781 Mb, LOD 6.2827 | chr 19 4.97811 Mb, LOD 6.11 | **reproduced** |
| K24 | gcg_KCl: QTL at chr 19 ~5 Mb, LOD 6.9, PWK high, NZO low | max LOD 2.97 at 7.57569 Mb | **not reproduced** |
| K25 | ins_GLP1: no QTL at chr 16 ~90.7 Mb | max LOD 3.90 at 92.7777 Mb | **reproduced** |

## Claim details

### K01: partly reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; 3.3G; Chr 1; 29.0228 Mbp; LOD 6.6069; A/J..WSB -0.04 0.22 -0.37 -0.04 -0.10 0.51 -0.18 0.00"
- Trait: `ins_3.3G` (N = 483)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 51.8047 Mb (support 25.359–55.7652) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.44 | paper's threshold | yes |
| LOD | 6.61 | 6.44 (difference -0.17) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | 129 > AJ > NOD > NZO > CAST > B6 > PWK > WSB (highest is 129, not CAST) | a single listed founder must be the extreme; several must all fall in that half | no |

Notes: Paper label '3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.04 0.22 -0.37 -0.04 -0.10 0.51 -0.18 0.00.

### K02: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; 3.3G | ins/islet; Chr 1; 29.0228 Mbp; LOD 7.0644; A/J..WSB -0.04 0.19 -0.40 -0.07 -0.07 0.51 -0.16 0.04"
- Trait: `ins_3.3G_per_content` (N = 482)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 29.0228 Mb (support 24.116–51.8093) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.21 | paper's threshold | yes |
| LOD | 7.06 | 6.21 (difference -0.85) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > B6 > WSB > NZO > AJ > NOD > PWK > 129 | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label '3.3G | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.04 0.19 -0.40 -0.07 -0.07 0.51 -0.16 0.04.

### K03: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; 8.3G | ins/islet; Chr 1; 29.0228 Mbp; LOD 6.1346; A/J..WSB -0.20 0.17 -0.34 -0.07 -0.12 0.47 0.03 0.05"
- Trait: `ins_8.3G_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 29.0228 Mb (support 25.2336–35.1432) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.87 | paper's threshold | no |
| LOD | 6.13 | 5.87 (difference -0.26) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > B6 > WSB > PWK > NOD > NZO > AJ > 129 | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label '8.3G | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.20 0.17 -0.34 -0.07 -0.12 0.47 0.03 0.05.

### K04: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; AA | ins/islet; Chr 1; 29.0228 Mbp; LOD 7.4243; A/J..WSB -0.27 0.11 -0.29 -0.12 -0.22 0.66 0.10 0.04"
- Trait: `ins_AA_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 29.0228 Mb (support 25.4623–36.141) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 7.76 | paper's threshold | yes |
| LOD | 7.42 | 7.76 (difference +0.34) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > PWK > B6 > WSB > NOD > NZO > AJ > 129 | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'AA | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.27 0.11 -0.29 -0.12 -0.22 0.66 0.10 0.04.

### K05: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; GLP1; Chr 1; 29.0228 Mbp; LOD 6.8223; A/J..WSB -0.27 0.21 -0.35 -0.02 -0.18 0.61 0.03 -0.03"
- Trait: `ins_GLP1` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 29.0228 Mb (support 27.8494–31.6568) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.62 | paper's threshold | yes |
| LOD | 6.82 | 6.62 (difference -0.20) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > B6 > PWK > NOD > WSB > NZO > AJ > 129 | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'GLP1'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.27 0.21 -0.35 -0.02 -0.18 0.61 0.03 -0.03.

### K06: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; GLP1 | ins/islet; Chr 1; 29.0228 Mbp; LOD 7.3471; A/J..WSB -0.26 0.20 -0.40 -0.05 -0.17 0.63 0.04 0.00"
- Trait: `ins_GLP1_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 29.0228 Mb | chr 1 29.0228 Mb (support 25.3747–31.4062) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 7.40 | paper's threshold | yes |
| LOD | 7.35 | 7.40 (difference +0.05) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > B6 > PWK > WSB > NOD > NZO > AJ > 129 | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'GLP1 | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.26 0.20 -0.40 -0.05 -0.17 0.63 0.04 0.00.

### K07: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: the Chr 1 locus at ~34 Mb (Ptpn18) affects secretion at 3.3 and 8.3 mM glucose, GLP1 and amino acids, with the CAST allele associated with increased secretion
- Quote: "QTL 1; AA; Chr 1; 33.8178 Mbp; LOD 6.9389; A/J..WSB -0.23 0.13 0.04 -0.25 -0.22 0.73 -0.25 0.05"
- Trait: `ins_AA` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 1 33.8178 Mb | chr 1 33.8178 Mb (support 27.8494–135.482) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 7.07 | paper's threshold | yes |
| LOD | 6.94 | 7.07 (difference +0.13) | ±1.00 | yes |
| founder pattern | high: CAST; low: — | CAST > B6 > 129 > WSB > NZO > NOD > AJ > PWK | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'AA'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.23 0.13 0.04 -0.25 -0.22 0.73 -0.25 0.05.

### K08: partly reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 5; GLP1 | 8.3G; Chr 2; 83.826 Mbp; LOD 7.5381; A/J..WSB -0.01 0.11 0.00 -0.06 -0.20 -0.15 0.08 0.24"
- Trait: `ins_GLP1_fc_8.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 2 83.826 Mb | chr 2 91.4305 Mb (support 76.0252–92.6618) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.39 | paper's threshold | yes |
| LOD | 7.54 | 6.39 (difference -1.15) | ±1.00 | no |

Notes: Paper label 'GLP1 | 8.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.01 0.11 0.00 -0.06 -0.20 -0.15 0.08 0.24.

### K09: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 8; KCl | 3.3G; Chr 3; 41.1508 Mbp; LOD 6.3472; A/J..WSB 0.04 -0.15 0.17 -0.20 -0.03 -0.18 0.11 0.24"
- Trait: `ins_KCl_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 41.1508 Mb | chr 3 70.0835 Mb (support 40.0319–73.5995) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.05 | paper's threshold | no |
| LOD | 6.35 | 5.05 (difference -1.30) | ±1.00 | no |

Notes: Paper label 'KCl | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.04 -0.15 0.17 -0.20 -0.03 -0.18 0.11 0.24.

### K10: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; GLP1 | 3.3G; Chr 3; 135.5183 Mbp; LOD 8.2587; A/J..WSB 0.08 0.00 0.01 0.38 -0.10 -0.23 -0.32 0.18"
- Trait: `ins_GLP1_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 135.518 Mb | chr 3 135.518 Mb (support 130.938–136.08) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 7.41 | paper's threshold | yes |
| LOD | 8.26 | 7.41 (difference -0.85) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > WSB > AJ > 129 > B6 > NZO > CAST > PWK | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'GLP1 | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.08 0.00 0.01 0.38 -0.10 -0.23 -0.32 0.18.

### K11: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; 16.7G | 3.3G; Chr 3; 135.5183 Mbp; LOD 7.3566; A/J..WSB 0.07 0.11 0.05 0.31 -0.05 -0.18 -0.47 0.16"
- Trait: `ins_16.7G_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 135.518 Mb | no called peak in window (max LOD in window 4.83) | ±5 Mb, or claimed position inside the observed support interval | no |
| threshold | LOD ≥ 6 | 4.83 | paper's threshold | no |

Notes: Paper label '16.7G | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.07 0.11 0.05 0.31 -0.05 -0.18 -0.47 0.16.

### K12: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; 8.3G | 3.3G; Chr 3; 135.2328 Mbp; LOD 6.8219; A/J..WSB 0.03 0.02 -0.07 0.28 -0.04 -0.16 -0.18 0.11"
- Trait: `ins_8.3G_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 135.233 Mb | chr 3 135.72 Mb (support 132.568–137.961) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.23 | paper's threshold | yes |
| LOD | 6.82 | 6.23 (difference -0.59) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > WSB > AJ > NZO > B6 > 129 > PWK > CAST | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label '8.3G | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.03 0.02 -0.07 0.28 -0.04 -0.16 -0.18 0.11.

### K13: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; AA | 3.3G; Chr 3; 136.0228 Mbp; LOD 6.727; A/J..WSB 0.06 0.05 0.08 0.32 -0.04 -0.19 -0.35 0.07"
- Trait: `ins_AA_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 136.023 Mb | chr 3 136.023 Mb (support 132.558–138.182) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.90 | paper's threshold | yes |
| LOD | 6.73 | 6.90 (difference +0.18) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > 129 > AJ > WSB > B6 > NZO > CAST > PWK | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'AA | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.06 0.05 0.08 0.32 -0.04 -0.19 -0.35 0.07.

### K14: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; 16.7G; Chr 3; 135.5183 Mbp; LOD 6.3817; A/J..WSB 0.08 0.17 0.07 0.21 -0.08 -0.22 -0.49 0.25"
- Trait: `ins_16.7G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 135.518 Mb | chr 3 133.553 Mb (support 126.027–143.168) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.86 | paper's threshold | no |
| LOD | 6.38 | 5.86 (difference -0.52) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > B6 > WSB > AJ > 129 > NZO > CAST > PWK | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label '16.7G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.08 0.17 0.07 0.21 -0.08 -0.22 -0.49 0.25.

### K15: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; PA | 3.3G; Chr 3; 135.5183 Mbp; LOD 6.3163; A/J..WSB 0.01 0.05 -0.01 0.24 -0.02 -0.14 -0.27 0.14"
- Trait: `ins_PA_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 135.518 Mb | no called peak in window (max LOD in window 3.47) | ±5 Mb, or claimed position inside the observed support interval | no |
| threshold | LOD ≥ 6 | 3.47 | paper's threshold | no |

Notes: Paper label 'PA | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.01 0.05 -0.01 0.24 -0.02 -0.14 -0.27 0.14.

### K16: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; 16.7G | ins/islet; Chr 3; 133.5613 Mbp; LOD 6.0938; A/J..WSB 0.13 0.17 0.10 0.19 -0.08 -0.28 -0.37 0.13"
- Trait: `ins_16.7G_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 133.561 Mb | chr 3 133.651 Mb (support 130.942–138.089) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.77 | paper's threshold | no |
| LOD | 6.09 | 5.77 (difference -0.33) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > AJ > B6 > 129 > WSB > NZO > CAST > PWK (not in upper half: WSB) | a single listed founder must be the extreme; several must all fall in that half | no |

Notes: Paper label '16.7G | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.13 0.17 0.10 0.19 -0.08 -0.28 -0.37 0.13.

### K17: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; PA; Chr 3; 133.6513 Mbp; LOD 6.0569; A/J..WSB 0.02 0.14 0.09 0.14 -0.02 -0.24 -0.26 0.13"
- Trait: `ins_PA` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 133.651 Mb | chr 3 133.651 Mb (support 132.558–148.414) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.64 | paper's threshold | no |
| LOD | 6.06 | 5.64 (difference -0.41) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > WSB > B6 > 129 > AJ > NZO > PWK > CAST | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'PA'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.02 0.14 0.09 0.14 -0.02 -0.24 -0.26 0.13.

### K18: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'; pattern from Results: Chr 3 ~135 Mb hotspot; CAST and PWK alleles associated with low, NOD and WSB with high secretion
- Quote: "QTL 9; PA | ins/islet; Chr 3; 133.6513 Mbp; LOD 6.1669; A/J..WSB 0.04 0.13 0.10 0.15 -0.01 -0.23 -0.28 0.09"
- Trait: `ins_PA_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 3 133.651 Mb | chr 3 133.651 Mb (support 130.934–148.099) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.52 | paper's threshold | no |
| LOD | 6.17 | 5.52 (difference -0.64) | ±1.00 | yes |
| founder pattern | high: NOD, WSB; low: CAST, PWK | NOD > B6 > 129 > WSB > AJ > NZO > CAST > PWK | a single listed founder must be the extreme; several must all fall in that half | yes |

Notes: Paper label 'PA | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.04 0.13 0.10 0.15 -0.01 -0.23 -0.28 0.09.

### K19: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 17; GLP1 | 8.3G; Chr 10; 102.4561 Mbp; LOD 6.0849; A/J..WSB -0.22 0.16 0.07 -0.05 0.02 0.09 -0.03 -0.05"
- Trait: `ins_GLP1_fc_8.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 10 102.456 Mb | chr 10 98.9982 Mb (support 88.9227–105.549) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.22 | paper's threshold | no |
| LOD | 6.08 | 5.22 (difference -0.86) | ±1.00 | yes |

Notes: Paper label 'GLP1 | 8.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.22 0.16 0.07 -0.05 0.02 0.09 -0.03 -0.05.

### K20: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 25; GLP1 | 8.3G; Chr 14; 78.899 Mbp; LOD 7.0659; A/J..WSB 0.01 0.04 -0.07 -0.30 -0.02 0.24 -0.03 0.13"
- Trait: `ins_GLP1_fc_8.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 14 78.899 Mb | chr 14 79.2106 Mb (support 78.6143–81.0268) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 5.97 | paper's threshold | no |
| LOD | 7.07 | 5.97 (difference -1.10) | ±1.00 | no |

Notes: Paper label 'GLP1 | 8.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.01 0.04 -0.07 -0.30 -0.02 0.24 -0.03 0.13.

### K21: not reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 26; KCl | 3.3G; Chr 16; 28.3788 Mbp; LOD 6.5976; A/J..WSB 0.13 0.05 -0.21 0.42 -0.06 -0.09 -0.10 -0.14"
- Trait: `ins_KCl_fc_3.3G` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 16 28.3788 Mb | no called peak in window (max LOD in window 3.94) | ±5 Mb, or claimed position inside the observed support interval | no |
| threshold | LOD ≥ 6 | 3.94 | paper's threshold | no |

Notes: Paper label 'KCl | 3.3G'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: 0.13 0.05 -0.21 0.42 -0.06 -0.09 -0.10 -0.14.

### K22: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 28; 8.3G | ins/islet; Chr 19; 4.9781 Mbp; LOD 6.3145; A/J..WSB -0.09 0.36 -0.04 -0.13 0.02 -0.41 0.08 0.21"
- Trait: `ins_8.3G_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 19 4.9781 Mb | chr 19 4.97811 Mb (support 3.98995–6.20552) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.26 | paper's threshold | yes |
| LOD | 6.31 | 6.26 (difference -0.05) | ±1.00 | yes |

Notes: Paper label '8.3G | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.09 0.36 -0.04 -0.13 0.02 -0.41 0.08 0.21.

### K23: reproduced

- Source: Supplemental Table 1 (JCI129143.sdt1.xlsx, sha256 659b3128...d88e), sheet 'ex vivo islet QTL'
- Quote: "QTL 28; GLP1 | ins/islet; Chr 19; 4.9781 Mbp; LOD 6.2827; A/J..WSB -0.08 0.33 -0.11 -0.09 0.03 -0.45 0.17 0.19"
- Trait: `ins_GLP1_per_content` (N = 478)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 19 4.9781 Mb | chr 19 4.97811 Mb (support 4.26737–6.20552) | ±5 Mb, or claimed position inside the observed support interval | yes |
| threshold | LOD ≥ 6 | 6.11 | paper's threshold | yes |
| LOD | 6.28 | 6.11 (difference -0.17) | ±1.00 | yes |

Notes: Paper label 'GLP1 | ins/islet'. Effects (A/J,B6,129,NOD,NZO,CAST,PWK,WSB) as printed: -0.08 0.33 -0.11 -0.09 0.03 -0.45 0.17 0.19.

### K24: not reproduced

- Source: Results text, glucagon secretion section
- Quote: "KCl-induced glucagon secretion QTL on Chr 19 at ~5 Mb, LOD 6.9 without conditioning on glucagon content (7.0 with)"
- Trait: `gcg_KCl` (N = 365)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| position | chr 19 5 Mb | no called peak in window (max LOD in window 2.97) | ±5 Mb, or claimed position inside the observed support interval | no |
| threshold | LOD ≥ 6 | 2.97 | paper's threshold | no |

Notes: Not in Supplemental Table 1. Uses the unconditioned value (6.9) on the raw glucagon trait.

### K25: reproduced

- Source: Results text, interim analysis (Hunk)
- Quote: "Chr 16 ~90.7 Mb GLP1-induced insulin secretion, LOD 7.4 at N = 300; 'At the completion of our study (N = 500) support for these QTL fell below our suggestive threshold'"
- Trait: `ins_GLP1` (N = 479)

| Check | Claimed | Observed | Tolerance | Pass |
|---|---|---|---|---|
| stays below threshold | max LOD < 6 | 3.90 at 92.7777 Mb | window ±5 Mb | yes |

Notes: Expected null at full N. Consistent with Supplemental Table 1 (no Chr 16 ~90 Mb row). By chance alone a null can cross LOD 6.

## Assumptions

1. Genotype probabilities: public attie_DO500_genoprobs_v5.rds (JAX). The paper does not say which genoprobs build it used; GRCm38 assumed.
2. Phenotypes from MPD Attie2, matched to the paper's trait labels by MPD measure number (trait_map.csv): 'X | 3.3G' and 'X | 8.3G' are MPD fold-change measures, 'X | ins/islet' is percent of islet insulin content, unlabelled traits are raw secretion.
3. Every trait is log-transformed (natural log), as the paper states; non-positive values become missing and are counted in the report.
4. Additive covariates sex and DOwave (factor), as stated; diet_days not used.
5. Allele effects by scan1blup, as the design specifies; the paper does not say which method it used.
6. No permutations in this run (the paper's fixed LOD 6 is the claim threshold); the design's 1,000-permutation check is deferred because of run time.
7. Covariates: sex, DOwave (as factors: DOwave)
8. Kinship: loco
9. Allele effects: scan1blup
10. Support interval: 1.5-LOD drop

## Inputs

| Input | Source | Retrieved | Bytes | sha256 |
|---|---|---|---|---|
| genoprobs | https://thejacksonlaboratory.box.com/shared/static/4hy4hbjyrxjbrzh570i4g02r62bx3lgk.rds | 2026-10-24T01:41:26Z | 1742822919 | `8d3126e87811421e7dd02a698203913686c5bb63591ed313a905bed612a02375` |
| map | https://raw.githubusercontent.com/smcclatchy/eqtl-mapping/16c0fbab55becb157e6bc22a8674d3f4686640b1/episodes/data/attie_do_map.rds | 2026-10-24T01:41:26Z | 830190 | `dbfd4220a7eb82b6f4949fa2dbac95ebb2eab8b9f969868f57b03e558f1f93de` |
| covar | https://raw.githubusercontent.com/smcclatchy/eqtl-mapping/16c0fbab55becb157e6bc22a8674d3f4686640b1/episodes/data/attie_do_covar.rds | 2026-10-24T01:41:26Z | 1789 | `c05df9c4980aa41ad42bde5981f653ffcebebdf3a83de488e22fd655eb01cb25` |
| mpd | https://phenome.jax.org/projects/Attie2/csvanimaldata | 2026-10-24T01:41:50Z | 442536 | `8e1a2b16dd4210b8cae1e98023d2d0533c046064d412c8698d2bd71b85e54dc3` |

## Environment

- Engine: qtl2, R version 4.4.3 (2025-02-28 ucrt), qtl2 0.46
- repro-check 0.1.0, Python 3.12.10
- Seed: 20261023; permutations: 0
- Samples: 500; markers: 68985
- Full R session info: `engine/session_info.txt`

## Ambiguities

- Zfp148: the Results text says the Chr 16 ~32 Mb KCl locus fell below LOD 6 at N = 500, while Supplemental Table 1 lists KCl | 3.3G on Chr 16 at 28.38 Mb, LOD 6.60. Claim K21 follows the table; no absence claim was made for Zfp148.
- Hunk (K25): the text says 'GLP1-induced secretion' without the transformation; the raw GLP1 trait is used.
- Glucagon (K24): the text gives LOD 7.0 conditioned on glucagon content and 6.9 without; the unconditioned trait and 6.9 are used.
- MPD lists about 240 mice per secretion measure while the paper mapped 479; the N actually mapped is shown per trait.
- MPD's description of measure Attie2:115 does not match its variable name; the variable name and measure number are used.
