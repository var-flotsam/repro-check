# Keller et al. 2019: what is public, and can the genome scan be rerun?

Paper: Keller MP, et al. "Gene loci associated with insulin secretion in islets
from nondiabetic mice." *J Clin Invest.* 2019;129(10):4419–4432.
doi:10.1172/JCI129143. Published 2019-09-09.

Checked: 2026-10-22. Status of each item is marked **verified** (I opened the
file or page and read it), **reported** (a page describes it but I could not
open the file), or **unknown**.

## 1. Short answer

A genome scan of the ex vivo insulin secretion traits looks reproducible from
public data, but not yet verified end to end. The inputs exist in three public
places that the authors or their collaborators maintain:

| Input | Where | Status |
|---|---|---|
| Genotype probabilities, 500 DO mice, 8 founders (`attie_DO500_genoprobs_v5.rds`) | JAX Box link used by the Carpentries "eQTL mapping" lesson | reported (download blocked from this sandbox) |
| Marker map, covariates (sex, wave, diet days), clinical phenotypes | Same lesson's GitHub repo, `smcclatchy/eqtl-mapping` | **verified** (downloaded, checksums below) |
| Ex vivo insulin secretion traits (7 secretagogues, 3 transformations), glucagon secretion | Mouse Phenome Database project **Attie2** (MPD:1020) | reported (CSV download failed here) |
| The authors' own LOD peaks and allele effects | Churchill lab QTL Viewer, "Attie Islet Secretion" | reported (interactive; files listed under "Download Data" were not readable from here) |
| Supplemental Table 1 (all QTL: trait, chr, position, LOD) | JCI supplement `JCI129143.sdt1.xlsx` | reported (download blocked here) |

The blocking issue in this session is the network, not the data: the sandbox
can reach GitHub, PyPI, conda and Docker Hub, but not jax.org, box.com,
phenome.jax.org or the JCI file host. See section 6.

## 2. What the paper says about its methods

From the article PDF (Methods, Results, figure legends):

- **Mice**: Diversity Outbred, HF/HS (Western-style) diet for 16 weeks; islets
  from 483 mice; QTL mapping in **479** mice (Figure 1–3 legends).
- **Genotyping**: "approximately 150,000 SNP loci". The array, genome build and
  Ensembl version are **not stated**. (150k matches GigaMUGA; the build is most
  likely GRCm38, which is what the lesson's map uses. To confirm in Phase 5.)
- **Traits**: insulin secretion at 3.3, 8.3 and 16.7 mM glucose; 40 mM KCl with
  3.3 mM glucose; 8.3 mM glucose + amino acids; 8.3 mM glucose + 100 nM GLP1;
  16.7 mM glucose + 0.5 mM palmitic acid. Glucagon secretion with KCl.
- **Transformations**: three per trait: (i) log secretion, (ii) log fractional
  secretion (percent of islet insulin content), (iii) log fold-change relative
  to the matching baseline glucose.
- **Model**: R/qtl2; kinship random effect with the LOCO method; **sex and
  wave as additive covariates**.
- **Thresholds**: suggestive LOD > 6.0; genome-wide significant LOD > 7.4
  (α = 0.05); per-trait thresholds "by permutation analysis" (count not
  stated).
- **Allele effects**: plotted, but the estimation method (BLUP or fixed
  coefficients) is **not stated**.
- **Data statement**: there is no formal data availability section. The text
  says all data are available in the QTL Viewer at
  <https://churchilllab.jax.org/qtlviewer/attie/islets>.

## 3. Checkable claims the text gives numbers for

These come from the article text; the full list with exact positions is in
Supplemental Table 1, which I could not open. Positions are approximate as
printed ("~"). All mapped in 479 mice unless noted.

| # | Locus | Trait(s) | Reported | Founder pattern |
|---|---|---|---|---|
| 1 | Chr 1 ~34 Mb (Ptpn18) | secretion at 3.3 and 8.3 mM glucose, GLP1, amino acids | QTL for all five traits incl. Ptpn18 local eQTL; no LOD in text | CAST high |
| 2 | Chr 3 ~135 Mb hotspot | 8.3/16.7 mM glucose, amino acids, PA | no LOD in text | CAST, PWK low; NOD, WSB high |
| 3 | Chr 3 ~41 Mb | KCl-induced insulin secretion | LOD 6.35 | not stated |
| 4 | Chr 2 ~84 Mb | GLP1 fold-change | LOD 7.5 | not stated |
| 5 | Chr 10 ~102 Mb | GLP1 fold-change | LOD 6.1 | not stated |
| 6 | Chr 14 ~79 Mb | GLP1 fold-change | LOD 7.1 | not stated |
| 7 | Chr 19 ~5 Mb | KCl-induced glucagon secretion | LOD 7.0 (6.9 without conditioning on glucagon content) | NZO low, PWK high (Results text) |
| 8 | Totals | all secretion traits | 60 QTL at LOD > 6, 5 above 7.4, merged to 25 insulin + 1 glucagon QTL | — |

### Important: Hunk and Zfp148 are not full-sample QTL

The Hunk and Zfp148 loci come from a **planned interim analysis at N = 300**:

- Chr 16 ~90.7 Mb, GLP1-induced secretion, LOD 7.4 → Hunk (gene at ~90.4 Mb).
- Chr 16 ~32 Mb, KCl-induced secretion, LOD 6.5 → Zfp148.

The paper then says: "At the completion of our study (N = 500) support for
these QTL fell below our suggestive threshold," and attributes this to the
winner's curse. So a faithful rerun on the full public data should **not**
find these two peaks above LOD 6. That is itself a checkable claim (a
"should not exceed" claim), and it is a good test that the tool does not
report agreement where there is none. Reproducing the N = 300 interim scan
would need the list of the first 300 mice. The paper does not give it, but
the public covariates have exactly five waves of 100 mice (`DOwave` 1–5), so
waves 1–3 are a plausible stand-in for the N = 300 point. That is an
assumption, and the report would have to label it as one.

Their validation in knockout and transgenic mice is wet-lab work and out of
scope.

## 4. Files I downloaded and checked

From `https://raw.githubusercontent.com/smcclatchy/eqtl-mapping/main/episodes/data/`
at commit `16c0fbab55becb157e6bc22a8674d3f4686640b1` (2026-10-19). Licence:
CC BY 4.0 (Carpentries lesson).

| File | sha256 | Contents |
|---|---|---|
| `attie_do_pheno.rds` | `4f48f220…d79f6` | 500 mice × 32 columns: demographics, oGTT, plasma glucose/insulin/TG, weights, islet count, insulin content. **No ex vivo secretion traits.** |
| `attie_do_pheno_dict.rds` | `d56f5ccd…f93de` | Dictionary for the above |
| `attie_do_covar.rds` | `c05df9c4…1cb25` | 500 mice: `mouse`, `sex`, `DOwave`, `diet_days` |
| `attie_do_map.rds` | `dbfd4220…f93de` | qtl2 marker map (list of chromosomes; needs R to inspect) |

Full hashes are in `docs/phase1/checksums.sha256`. Mouse IDs look like
`DO021`; 483 mice have `diet_days`, which matches the 483 islet donors.

Also listed by the lesson but not downloaded yet: kinship, raw and
normalised islet RNA-seq, eQTL peaks, and genoprobs from
`https://thejacksonlaboratory.box.com/shared/static/4hy4hbjyrxjbrzh570i4g02r62bx3lgk.rds`.

## 5. Sources and terms of use

| Source | Terms | Notes |
|---|---|---|
| JCI article and supplement | Free to read; JCI's reuse terms apply | We cite numbers, we don't redistribute the PDF |
| Carpentries lesson data (GitHub) | CC BY 4.0 | Attribute the lesson and Keller et al. |
| JAX Box genoprobs | No licence stated on the link | Fetch at run time, don't re-host; record checksum |
| MPD Attie2 (MPD:1020) | MPD terms of use (<https://phenome.jax.org/about/termsofuse>) | Cite Keller 2018 Genetics and the MPD project; MPD notes genotypes are "available at DODB" |
| Dryad doi:10.5061/dryad.pj105 | Dryad publishes under CC0 | 1.83 GB `Attie_DO378_eQTL_viewer_v1.Rdata`: 378-mouse eQTL viewer object from Keller 2018 *Genetics*. Probably not the 479-mouse secretion set |
| QTL Viewer | No terms stated | Its "Download Data" table loads by script; I could not list it from here |

All of this is mouse data, public and open access. None is controlled-access.

## 6. What stops a rerun today, and what fixes it

1. **Network access.** Downloads from jax.org, box.com, phenome.jax.org and
   cloudfront.net (JCI files) are refused by this environment's network policy.
   Adding those hosts to the allowed domains would let me fetch them. R itself
   can come from conda-forge (`r-qtl2` is packaged there) or Docker Hub
   (rocker), both of which are reachable.
2. **Sample matching.** I need to confirm the MPD Attie2 animal IDs match the
   `DO###` IDs in the genoprobs. MPD lists N ≈ 240 for each secretion measure
   with sex "both". The public covariates have 251 females and 249 males, so
   240 is probably a per-sex count (≈ 480 total, close to the paper's 479), but
   it could be a subset. **Unknown until I can open the CSV.**
3. **Exact trait definitions.** The fold-change and percent traits in MPD need
   to match the paper's three transformations; the names suggest they do.
4. **Genoprobs version.** `v5` may have been rebuilt after 2019 (for example a
   new marker set or build). Small shifts in peak position and LOD would follow.
   The tolerances must allow for this, and the report must say so.

## 7. Proposed honest target for Stage C

Not "rerun the paper", but: **rerun the paper's stated R/qtl2 model on the
public 500-mouse genoprobs and the MPD secretion traits, and check the
specific peaks the paper reports with numbers.** Concretely:

- Claims 1–7 above: is there a peak on the stated chromosome within ±X Mb of
  the stated position, with LOD within ±Y, and the same high/low founders?
- The two "should not exceed" claims: Chr 16 ~90.7 Mb (GLP1) and ~32 Mb (KCl)
  stay below LOD 6 at full N.
- The summary count (60 QTL above LOD 6) only as a secondary, loosely toleranced
  claim, because it depends on peak-calling rules the paper does not give.
- As a cross-check, compare our peaks with the authors' own peaks in the QTL
  Viewer (if its files are downloadable). That checks "same data, same software"
  separately from "matches the paper".

Tolerances (proposed, to be set in design.md before any run): position within
the paper's rounding plus a 1.5-LOD support interval or ±5 Mb, whichever is
wider; LOD within ±1.0; founder pattern = same top and bottom founders. These
are placeholders for your review, not decisions.

Out of scope: the eQTL and mediation analyses (need the RNA-seq; possible
later), the human GWAS enrichment, and all knockout and transgenic mouse
validation.
