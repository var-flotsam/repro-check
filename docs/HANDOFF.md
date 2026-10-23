# HANDOFF

Last updated: 2026-10-23, end of Phase 4.

## Project

repro-check: a Claude skill (plus scripts, maybe an MCP server later) that
reruns published mouse and human genetics analyses from public data in a
pinned environment and reports, claim by claim, whether results come back
within tolerances set before the run. Flagship: Keller et al. 2019 JCI
(doi:10.1172/JCI129143). Owner: Ethan (GitHub `var-flotsam`).

## Rules from the owner

- Public, open-access mouse and human data only. No pathogens, toxins, or
  designing or modifying organisms or sequences.
- Never declare a result reproduced on the model's judgment.
- Commit after each phase as "Phase N: ..."; **ask before pushing**.
- docs/design.md needs the owner's approval before Phase 3.
- Ask, don't guess.

## Status

| Phase | State |
|---|---|
| 1. Docs, prior art, data availability | Done. Owner approved the Stage C target (2026-10-22) |
| 2. design.md | Approved by owner 2026-10-23 (section 10 points taken at their defaults, see below) |
| 3. Synthetic tests and skeleton | Done |
| 4. R/qtl2 warm-up | Done: iron 10/11 reproduced, DOex 1/1 reproduced (see below) |
| 5–7 | Not started |

Repository: https://github.com/var-flotsam/repro-check (branch `main`).
Phases 1–2 were pushed 2026-10-22 with the owner's OK; the owner later approved
pushing each phase to this repo ("yes to all"). Licence: MIT (owner, 2026-10-23).

## Phase 1 outputs

- `docs/phase1/keller2019-data-availability.md`: what is public, the claims the
  paper gives numbers for, and the proposed Stage C target.
- `docs/phase1/agent-skills-and-mcp.md`: requirements from the current docs.
- `docs/phase1/prior-art.md`
- `docs/phase1/checksums.sha256`: inputs downloaded so far.

## Key findings to carry forward

- Inputs: genoprobs `attie_DO500_genoprobs_v5.rds` (JAX Box, via the
  Carpentries eQTL lesson), map, covariates and clinical phenotypes
  (`smcclatchy/eqtl-mapping` on GitHub, CC BY 4.0), and ex vivo secretion traits
  (MPD project Attie2).
- Model per paper: R/qtl2, LOCO kinship, sex and wave additive covariates,
  479 mice; LOD > 6 suggestive, > 7.4 significant.
- Hunk and Zfp148 came from an N = 300 interim scan and fell **below** LOD 6
  at full N, per the paper. Treat them as expected nulls at full N.
- Covariates show 5 waves × 100 mice; waves 1–3 may stand in for the interim set
  (unconfirmed assumption).

## Blockers

- The session's network policy blocks jax.org, box.com, phenome.jax.org and
  the JCI file host (cloudfront.net). GitHub, PyPI, conda and Docker Hub work.
  The owner set a new default cloud environment on 2026-10-22 (presumably
  allowing these hosts). It applies only to new sessions: the Phase 1–2 session
  still could not reach them at 23:59 UTC. Run Phase 4–5 data fetches from a
  thread started on the new environment.

## Phase 3 outputs

- Python package `repro_check` (uv-locked): `claims.py` (schema, freeze, hash),
  `compare.py` (all verdict logic), `fetch.py` (manifest, sha256),
  `run.py` (calls R), `report.py`, `cli.py`.
- R engine `src/repro_check/engines/qtl2/{lib,engine,simulate}.R`.
- R env: `env/r-environment.yml` (exact pins) and `env/r-linux-64.lock`;
  `scripts/make_r_env.py PREFIX` installs it with py-rattler (no conda needed).
- Stage A: `examples/stage_a/` — S1–S3 planted QTL reproduced, S4–S5 nulls
  held, S6–S7 false claims rejected. 61 pytest + 15 testthat checks pass.
- `skill/repro-check/SKILL.md` + `reference/claims.md`, `reference/qtl2.md`.
- CI: `.github/workflows/ci.yml` (unit tests; R + Stage A).

## Phase 4 outputs

- Engine can now build genoprobs from a raw qtl2 cross (`cross`, `genoprob`,
  `xcovar`), report on another map (`report_map`), and compute permutation
  thresholds (`n_perm`, `perm_alpha`); new claim kind `perm_threshold`;
  `paper.position_units` (Mb or cM); tolerance `pos_ci` (0 = position must
  match by distance only).
- `examples/stage_b_iron/` (qtl2 `iron` F2 at kbroman/qtl2@3329fb52, claims
  B1–B11 from the R/qtl2 user guide) and `examples/stage_b_doex/` (DOex at
  rqtl/qtl2data@8cfeb3ca, claim D1). Claims confirmed by the owner via a
  decision card and frozen 2026-10-23T01:41Z.
- Reports: `docs/results/stage_b_iron.md`, `docs/results/stage_b_doex.md`
  (with the frozen claims files beside them).
- Results: all five iron peaks and both counts reproduced to the marker; three
  of four permutation thresholds reproduced. **B8** (liver, alpha 0.05) came
  back 3.30 vs 3.46, outside ±0.15, so it is *not reproduced*. Left as
  recorded: tolerances are never changed after freezing. DOex D1 reproduced
  (chr 2 96.84 Mb, LOD 10.97).
- Lesson: ±0.15 LOD is tighter than the Monte Carlo spread of a 1000-permutation
  alpha 0.05 quantile. For future perm claims use about ±0.25, or base the
  tolerance on the permutation count.
- `tests/test_stage_b.py` (markers `r` and `network`) reruns both warm-ups
  without permutations. 71 pytest pass locally.

## Decisions taken without an explicit answer

Design section 10 was approved as a whole, so: default tolerances as
drafted; skill name kept as `repro-check`; the N = 300 interim scan
(waves 1–3) is not yet included and will be offered as optional when Phase 5
claims are drafted.

## Notes for the next phase

- CI installs R from `env/r-linux-64.lock` with the runner's conda (green
  since run 3). An env made with `scripts/make_r_env.py` (py-rattler) worked in
  the cloud session but failed on the GitHub runner (`tools` namespace would
  not load); cause not found. Prefer the lock file with conda/micromamba.

- A null-trait sim showed 1 of 20 noise traits crossing LOD 6 on a small
  genome: expected nulls can fail by chance. Keep this in mind for the
  Hunk/Zfp148 absence claims and say it in the report.
- Phase 5 (Keller 2019) needs jax.org/box.com/phenome.jax.org/cloudfront.net.
  Run it from a session on the new environment or on the owner's machine.
  Draft claims from docs/phase1/keller2019-data-availability.md, offer the
  optional N = 300 interim scan, and get the owner's confirmation before
  freezing.

## Open questions for the owner

Where Phase 5 should run (new cloud environment or the owner's machine).
