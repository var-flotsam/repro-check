# repro-check design

Status: approved 2026-10-23; section 11 (figures) added 2026-10-24.

## 1. Principles

1. **Verdicts are computed.** A script compares each result with its claim and
   tolerance. The model extracts claims, runs steps and writes prose. It never
   decides agreement.
2. **Freeze before running.** Claims and tolerances are written to
   `claims.yaml`, confirmed by the user, and hashed (sha256) before any data
   is fetched. Changing the file after the hash is recorded voids the run.
3. **Everything recorded.** Every input has a source URL, retrieval time and
   sha256. Every tool has a pinned version. Every random seed is fixed. Every
   choice the paper doesn't specify is written down as an assumption.
4. **Expected nulls count.** A claim can say a peak should be *absent*. These
   catch a pipeline that finds whatever it is told to look for.
5. **Neutral reporting.** A result is reproduced or not; the report never
   speculates about author error.
6. **Scope.** Public, open-access mouse and human genetics and expression data
   only. No controlled-access data, no pathogen or toxin work, nothing about
   designing or modifying organisms or sequences. The skill refuses runs
   outside this.

## 2. Architecture

```
skill/repro-check/
  SKILL.md                 workflow for Claude (<500 lines, portable frontmatter)
  reference/claims.md      claim schema and how to write tolerances
  reference/qtl2.md        R/qtl2 conventions, DO-specific assumptions
  scripts/  -> the Python package's CLI entry points
src/repro_check/           Python package (uv-pinned)
  claims.py                load, validate, freeze, hash claims.yaml
  fetch.py                 download per manifest, verify sha256, refuse on mismatch
  run.py                   call engines, collect results.json
  compare.py               tolerance rules -> verdicts (pure functions)
  report.py                Markdown report from verdicts + provenance
  engines/qtl2/            R scripts driven by Python (scan1, find_peaks, effects)
r/                         renv.lock or conda env for R/qtl2
tests/                     pytest; tests/testthat for R
evals/                     eval papers, frozen claims, expected verdicts
```

CLI: `repro-check init | freeze | fetch | run | compare | report`. Each step
reads the previous step's files from `runs/<run_id>/` and writes its own, so
a run can be resumed and audited.

**Skill first, MCP later.** Claude Code runs the CLI. An MCP server (stdio,
spec 2026-07-28, Tasks extension for long scans, `outputSchema` on each tool)
is added only if we need it for other clients. It would wrap the same CLI.

**Environment.** Python via `uv` (`uv.lock`). R 4.x with `qtl2` from
conda-forge, pinned in an environment lock file, or a pinned rocker image by
digest. I'll choose whichever installs reliably in CI. The run records
`sessionInfo()` and `uv pip freeze` output.

## 3. Stages

| Stage | Data | Purpose | Pass bar |
|---|---|---|---|
| A. Synthetic | Simulated DO-like crosses with planted QTL (known chr, Mb, effect); simulated count matrices for expression | Prove compare.py and the engine recover known answers, and that nulls stay null | Planted peaks within tolerance; no false peaks above threshold in null sims at the expected rate |
| B. Warm-up | R/qtl2's example data (`iron`, and the DO example from qtl2data) with results published in the qtl2 docs | Real data, known published numbers, small and fast | All chosen claims reproduced |
| C. Keller 2019 | Public genoprobs (500 DO), map, covariates, MPD Attie2 secretion traits | Flagship | Report, whatever the verdicts |

## 4. Claim schema (`claims.yaml`)

```yaml
paper:
  doi: 10.1172/JCI129143
  citation: Keller MP et al. J Clin Invest 2019;129(10):4419-4432
frozen: {by: Ethan, at: 2026-10-23T00:00:00Z, sha256: <filled by freeze>}
claims:
  - id: C1
    kind: qtl_peak                # qtl_peak | qtl_absent | count | effect_pattern
    source: "Results p.4423; Fig 3A"   # where in the paper
    quote: "a QTL ... at ~34 Mb"       # short verbatim text
    trait: INS_GLU8p3_GLP1        # dataset column after transformation
    transform: log
    chr: "1"
    pos_mb: 34
    pos_reported_precision_mb: 1  # "~34" means rounding to the nearest Mb
    lod: null                     # null when the paper gives no number
    founders_high: [CAST]
    founders_low: []
    tolerance:
      pos_mb: 5
      lod_abs: 1.0
      threshold_lod: 6.0          # peak must clear this to count as found
    notes: ""
```

Kinds:

- `qtl_peak`: there is a peak on `chr` above `threshold_lod` within
  `pos_mb ± tol`, and its LOD (if stated) and founder pattern (if stated)
  match.
- `qtl_absent`: the maximum LOD within `pos_mb ± tol` stays below
  `threshold_lod` (for Hunk and Zfp148 at full N).
- `effect_pattern`: the founders with the highest and lowest coefficients at
  the peak match the listed founders.
- `count`: a number (for example "60 QTL above LOD 6") within a relative
  tolerance. Secondary only.

## 5. Tolerance rules

Each tolerance is set when claims are frozen, with a written reason. Defaults
(the user can change them before freezing):

| Quantity | Default | Reason |
|---|---|---|
| Peak position | ± max(5 Mb, the paper's rounding, the 1.5-LOD support interval half-width) | DO peaks are typically resolved to a few Mb; genoprobs version and marker set can shift them |
| LOD | ± 1.0, or ± 15% when LOD > 10 | Different genoprobs builds, kinship and missing-data handling shift LOD by around this much |
| Threshold crossing | Same threshold as the paper | No moving the goalposts |
| Founder pattern | Top founder and bottom founder must match; for lists of several founders, all listed founders must be in the upper (or lower) half | Effects are noisy, and the paper describes them qualitatively |
| Count claims | ± 20% | Peak-calling rules are under-specified |

Verdict per claim, from the checks that apply (position, LOD, pattern,
threshold):

- **reproduced**: every applicable check passes.
- **partly reproduced**: the peak is found (position and threshold pass) but
  at least one other check fails (LOD or pattern).
- **not reproduced**: position or threshold fails. For `qtl_absent`, a peak
  crosses the threshold.
- **not checkable**: the inputs needed are missing (for example a trait not in
  the public data). This is never counted as reproduced.

Every verdict lists the observed values next to the claimed ones and the
tolerance used.

## 6. Keller 2019 assumptions to record

Where the paper is silent, the run uses these and the report lists them:

- Genome build GRCm38 and the public `v5` genoprobs (the paper doesn't say
  which genoprobs were used).
- Additive covariates: sex and `DOwave`, as stated; `diet_days` not used.
- Kinship: LOCO from the same genoprobs (`calc_kinship(type="loco")`).
- Thresholds: the paper's fixed LOD 6 and 7.4. Permutations (1,000, seed fixed)
  are run as a check, not as the claim threshold.
- Allele effects: `scan1blup` (common for DO); `scan1coef` reported alongside.
- Transformations: log, log of percent of content, log fold-change, matched to
  MPD columns by name; the mapping table is written out in the report.
- Interim set (only if we check the N = 300 claims): waves 1–3.

## 7. Report format (`report.md`)

1. Header: paper, run id, date, claims hash, overall counts.
2. Results table: claim id, short claim, claimed vs observed, tolerance,
   verdict.
3. Per-claim detail: quote and location in the paper, numbers, LOD plot path.
4. Assumptions (numbered).
5. Inputs: URL, retrieved time, size, sha256.
6. Environment: R and package versions, Python lock hash, container digest,
   seeds.
7. Ambiguities: places where the paper could be read more than one way, and
   which reading was used.

Wording is neutral ("not reproduced within the stated tolerance"), with no
claims about why.

## 8. Testing and evals

- **pytest**: compare.py verdict logic on hand-made cases (including the edge
  at exactly the tolerance), claims validation, freeze and hash, fetch
  checksum refusal, report rendering.
- **testthat**: the R engine on small simulated crosses with planted QTL.
- **CI** (GitHub Actions): Stage A and unit tests only; no large downloads.
- **Evals** (Phase 6): five or more published analyses with known outcomes,
  including at least one with a documented failure to replicate. Each has
  frozen claims and expected verdicts. Metrics: accuracy of verdicts, and the
  **false "reproduced" rate**, reported first. A false "reproduced" verdict
  fails the eval suite. Candidate papers are chosen in Phase 6 and listed for
  approval.

## 9. Workflow in SKILL.md

1. Check scope (species, data access). Stop if out of scope.
2. Extract candidate claims from the paper into `claims.yaml` with quotes and
   locations. Show them to the user and **wait for confirmation**.
3. `freeze` (writes the hash).
4. `fetch`, `run`, `compare`, `report`.
5. Show the report. Never restate a verdict differently from compare.py's
   output.

## 10. Open points for you

1. Are the default tolerances in section 5 right, or do you want them tighter?
2. Should Stage C include the N = 300 interim scan (waves 1–3), so the Hunk
   and Zfp148 peaks are checked as positive claims too? It rests on an
   assumption about which mice were in the interim set.
3. The skill name: `repro-check`, or the recommended gerund form
   `checking-reproducibility`?

## 11. Figures (added 2026-10-24 at the owner's request)

The skill also redraws the paper's figures from the numbers it computed, so a
reader can put the paper's figure and ours side by side.

**Rules**

1. **A figure gets no verdict.** Whether two plots "look the same" is a
   judgment, and principle 1 says the model never makes one. Each redrawn
   figure is labelled "regenerated from this run; compare by eye; no verdict".
   The report never says a figure was reproduced.
2. **What a figure shows numerically becomes a claim.** If a figure shows a
   peak, an effect sign or a threshold, that number is written as an ordinary
   claim (with the figure as its `source`) and checked by `compare.py`.
3. **Figures are declared before the run.** A `figures:` list in the claims
   file names each paper figure (number and panel), what to draw, the traits
   and the region. It is frozen and hashed with the claims, so the set of
   figures can't be chosen after seeing the results. (Files without
   `figures:` hash as before, so earlier frozen files stay valid.)
4. **Same axes as the paper.** Units, trait transformation, chromosome range
   and founder colours follow the paper where it states them; where it
   doesn't, the choice is listed under assumptions.
5. **We never copy the paper's figure images** (journal copyright). The
   report links to the figure by number and URL.

**Figure kinds (R/qtl2 engine)**

| kind | draws | from |
|---|---|---|
| `genome_scan` | LOD across all chromosomes, threshold lines | `lod_profile.csv.gz` |
| `lod_chr` | LOD on one chromosome or region, support interval shaded | `lod_profile.csv.gz` |
| `allele_effects` | founder effects (CC colours) along a region, LOD below | engine `effects_<id>.csv` |
| `peak_map` | every called peak by trait and position (like a QTL heat map) | `results.json` |

Output: `RUN/figures/<id>.png` and `.pdf`, plus the data behind each figure as
CSV, listed in a "Figures" section of the report.

**Where it fits in the plan.** This is built and tried on Stage B and Keller
(the Keller run data is on the owner's PC) before Phase 6. In Phase 6 each eval
paper declares its figures too. Evals score only verdicts, so figures don't
change the false "reproduced" rate. They do add one check: the report must
never put a verdict on a figure.
