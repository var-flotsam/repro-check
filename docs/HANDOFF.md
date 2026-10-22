# HANDOFF

Last updated: 2026-10-22, Phase 2 drafted.

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
| 2. design.md | Drafted and committed; **awaiting owner approval** |
| 3–7 | Not started |

Repository: https://github.com/var-flotsam/repro-check (branch `main`).
Phases 1–2 were pushed 2026-10-22 with the owner's OK.

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
  The owner can add hosts in the project's cloud environment settings.
- R is not installed; plan to use conda-forge `r-qtl2` or a rocker image.

## Open questions for the owner

1. Approve docs/design.md (and its section 10 points).
2. Add the blocked hosts to the cloud environment's allowed domains. Owner said
   yes; the hosts were still blocked at 23:51 UTC.
