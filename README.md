# repro-check

A Claude skill that reruns published mouse and human genetics analyses from
public data in a pinned environment and reports which results come back,
using numeric tolerances fixed before the run. The model never decides
agreement; `repro_check.compare` does.

Work in progress (Phase 5 of 7). Design: [docs/design.md](docs/design.md).
Status and open questions: [docs/HANDOFF.md](docs/HANDOFF.md).

## Layout

- `skill/repro-check/`: the skill (`SKILL.md` plus reference notes)
- `src/repro_check/`: Python CLI (`validate`, `freeze`, `fetch`, `run`,
  `compare`, `report`, `simulate`) and the R/qtl2 engine scripts
- `env/`: pinned R environment (R 4.4.3, qtl2 0.46, conda-forge lock)
- `examples/stage_a/`: synthetic cross with planted QTL, expected nulls and
  deliberately false claims
- `examples/stage_b_iron/`, `examples/stage_b_doex/`: R/qtl2 example data
  warm-ups; reports in `docs/results/`
- `tests/`, `r/tests/testthat/`: pytest and testthat

## Quick start

```bash
uv sync --group dev
uv run --group renv python scripts/make_r_env.py .renv
export PATH="$PWD/.renv/bin:$PATH"
uv run pytest -q                  # unit tests + Stage A through R
uv run bash examples/stage_a/run.sh   # writes runs/stage_a/report.md
```

## Warm-up results (Phase 4)

| Dataset | Claims | Reproduced | Not reproduced |
|---|---|---|---|
| qtl2 `iron` F2 (R/qtl2 user guide) | 11 | 10 | 1 (B8: liver permutation threshold 3.30 vs 3.46, tolerance ±0.15) |
| qtl2data `DOex` | 1 | 1 | 0 |

Full reports: [iron](docs/results/stage_b_iron.md), [DOex](docs/results/stage_b_doex.md).

## Keller et al. 2019 (Phase 5)

25 claims from the paper's Supplemental Table 1 and Results text, frozen
before any data was fetched, rerun on the public 500-mouse genoprobs and MPD
Attie2 traits: **11 reproduced, 2 partly reproduced, 12 not reproduced**.
Full report: [docs/results/stage_c_keller.md](docs/results/stage_c_keller.md).
