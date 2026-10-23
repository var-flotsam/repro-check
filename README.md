# repro-check

A Claude skill that reruns published mouse and human genetics analyses from
public data in a pinned environment and reports which results come back,
using numeric tolerances fixed before the run. The model never decides
agreement; `repro_check.compare` does.

Work in progress (Phase 3 of 7). Design: [docs/design.md](docs/design.md).
Status and open questions: [docs/HANDOFF.md](docs/HANDOFF.md).

## Layout

- `skill/repro-check/`: the skill (`SKILL.md` plus reference notes)
- `src/repro_check/`: Python CLI (`validate`, `freeze`, `fetch`, `run`,
  `compare`, `report`, `simulate`) and the R/qtl2 engine scripts
- `env/`: pinned R environment (R 4.4.3, qtl2 0.46, conda-forge lock)
- `examples/stage_a/`: synthetic cross with planted QTL, expected nulls and
  deliberately false claims
- `tests/`, `r/tests/testthat/`: pytest and testthat

## Quick start

```bash
uv sync --group dev
uv run --group renv python scripts/make_r_env.py .renv
export PATH="$PWD/.renv/bin:$PATH"
uv run pytest -q                  # unit tests + Stage A through R
uv run bash examples/stage_a/run.sh   # writes runs/stage_a/report.md
```
