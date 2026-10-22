# Prior art, and how repro-check differs

Surveyed 2026-10-22. Short list, grouped by what each does.

## Workflow and environment tools

| Tool | What it gives | What it doesn't |
|---|---|---|
| Snakemake, Nextflow (nf-core), CWL/WDL | Re-runnable pipelines with pinned containers and provenance | You must already have the pipeline. They don't read a paper, and don't say whether the result matches it |
| renv, uv, conda/pixi, Docker/Apptainer | Pinned software environments | Same: environment only |
| Code Ocean, Whole Tale, Binder, ReproZip | Packaged "capsules" of an author's own code | Need the authors to have deposited runnable code; Keller 2019 did not |

repro-check uses these (renv or conda for R, uv for Python, a container) as
parts. They are the "pinned environment", not the competitor.

## Benchmarks of agents reproducing research

- **CORE-Bench** (Siegel et al., 2024, arXiv:2409.11363): agents reproduce
  results from code capsules with author code supplied. Graded on answers to
  questions about outputs.
- **PaperBench** (OpenAI, 2025) and **RECLAIM** (Salunkhe et al., Sept 2026,
  arXiv:2609.28850): ML papers. RECLAIM pins one result per paper with a stated
  tolerance, but grading is done by an LLM auditor scoring evidence 0–10. Its
  key finding for us: agents **overclaim**. They self-reported success on 128
  runs; the auditor confirmed 73.
- **BixBench** (2025, arXiv:2503.00096): open-ended computational biology
  questions on real datasets. It tests analysis skill, not agreement with a
  specific paper.
- **SEER-Repro** (Liu et al., Oct 2026, arXiv:2610.23845): an agent reproduces
  2,190 atomic claims from 20 cancer-registry papers, with 77% reproduced, and
  flags analytic choices that change results. Closest in spirit, in
  epidemiology, not genetics.

## Agents for bioinformatics

- **Paper2Agent** (Miao, Davis, Zhang, Pritchard, Zou; Stanford, 2025,
  arXiv:2509.06917): turns a paper plus **its codebase** into an MCP server,
  testing tools against the paper's figures. Genomics case studies (AlphaGenome,
  Scanpy, TISSUE). Requires author code.
- **Biomni** and similar general biomedical agents: broad tool use, no
  claim-by-claim verdicts.

## Genetics-specific

- **R/qtl2** (Broman et al.) and its vignettes are the reference implementation
  for DO mapping, and the source of our Stage B data.
- **QTL Viewer / qtl2web** (Churchill lab; Vincent et al. 2022): serves the
  authors' own scans interactively. It shows what the authors computed; it does
  not rerun from raw inputs or compare with the paper's text.
- **Carpentries "eQTL mapping" lesson**: teaches mapping on this exact Attie
  dataset. It is a teaching path, not a verification tool, but it is how the
  public inputs are packaged.

## How repro-check differs

1. **Verdicts are computed, never judged.** Every claim has a numeric
   tolerance fixed and confirmed by a person before the run, and a script
   decides reproduced, partly reproduced, or not reproduced. RECLAIM's
   overclaiming result is the reason: an LLM grader, or the agent itself, is
   the weakest link.
2. **No author code needed.** It reruns the paper's stated method from public
   data (like SEER-Repro, unlike CORE-Bench and Paper2Agent), and records every
   assumption where the methods are silent.
3. **"Should not reproduce" claims.** Some claims are expected nulls (for
   example Hunk and Zfp148 falling below threshold at full N). The tool checks
   these too, which guards against confirming whatever is asked.
4. **Scored on the worst error.** Evals count false "reproduced" verdicts
   separately and treat them as the main failure metric.
5. **Narrow domain on purpose.** Mouse and human statistical genetics, R/qtl2
   first, with tolerance rules that make sense for QTL peaks (Mb, LOD, founder
   effects).

Gaps I didn't fill: I didn't read the full text of PaperBench, BixBench or
Biomni; the descriptions above come from abstracts and summaries.
