"""Run an engine on fetched inputs.

Run config (YAML) for the qtl2 engine:

    engine: qtl2
    genoprobs: input:genoprobs      # "input:NAME" refers to a fetched input
    map: input:map
    pheno: input:pheno
    covar: input:covar              # optional; defaults to pheno
    id_column: mouse
    traits:
      - {name: ins_glp1, column: INS_GLU8p3_GLP1, transform: log}
    addcovar: [sex, DOwave]
    covar_factors: [DOwave]
    kinship: loco
    report_threshold: 3
    peakdrop: 1.5
    ci_drop: 1.5
    effects: blup
    n_perm: 0
    seed: 20261023
    assumptions: ["..."]            # copied into the report
    ambiguities: ["..."]

The R script path, the Rscript used and the package versions are recorded in
RUN/environment.json.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata, resources
from pathlib import Path
from typing import Any

import yaml

ENGINE_KEYS = {
    "genoprobs", "map", "pheno", "covar", "id_column", "traits", "addcovar", "covar_factors",
    "kinship", "report_threshold", "peakdrop", "ci_drop", "effects", "n_perm", "seed",
    "subset", "chromosomes", "cores",
}
REPORT_KEYS = {"engine", "assumptions", "ambiguities", "description"}


class RunError(RuntimeError):
    pass


def engine_dir() -> Path:
    return Path(str(resources.files("repro_check") / "engines" / "qtl2"))


def rscript() -> str:
    exe = os.environ.get("REPRO_CHECK_RSCRIPT") or shutil.which("Rscript")
    if not exe:
        raise RunError("Rscript not found. Install the pinned R environment "
                       "(see env/r-environment.yml) and put its bin/ on PATH, "
                       "or set REPRO_CHECK_RSCRIPT.")
    return exe


def _resolve(value: Any, run_dir: Path, provenance: dict[str, Any]) -> Any:
    if isinstance(value, str) and value.startswith("input:"):
        name = value.removeprefix("input:")
        try:
            return str((run_dir / provenance["inputs"][name]["path"]).resolve())
        except KeyError:
            raise RunError(f"run config refers to input {name!r}, which was not fetched") from None
    return value


def build_engine_config(cfg: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    unknown = set(cfg) - ENGINE_KEYS - REPORT_KEYS
    if unknown:
        raise RunError(f"unknown run config key(s): {sorted(unknown)}")
    if cfg.get("engine", "qtl2") != "qtl2":
        raise RunError(f"unsupported engine {cfg.get('engine')!r}; only qtl2 exists so far")
    for key in ("genoprobs", "map", "pheno", "traits"):
        if key not in cfg:
            raise RunError(f"run config needs {key!r}")
    if "seed" not in cfg:
        raise RunError("run config needs an explicit 'seed'")
    prov_path = run_dir / "provenance.json"
    provenance = json.loads(prov_path.read_text()) if prov_path.exists() else {"inputs": {}}
    out = {k: _resolve(v, run_dir, provenance) for k, v in cfg.items() if k in ENGINE_KEYS}
    out["out_dir"] = str((run_dir / "engine").resolve())
    return out


def run(config: str | Path, run_dir: str | Path) -> Path:
    config = Path(config)
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(config.read_text()) or {}
    engine_cfg = build_engine_config(cfg, run_dir)
    (run_dir / "run_config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
    cfg_path = run_dir / "engine_config.json"
    cfg_path.write_text(json.dumps(engine_cfg, indent=2))
    exe = rscript()
    proc = subprocess.run([exe, str(engine_dir() / "engine.R"), str(cfg_path)],
                          capture_output=True, text=True)
    (run_dir / "engine.log").write_text(proc.stdout + proc.stderr)
    if proc.returncode != 0:
        raise RunError(f"engine failed (exit {proc.returncode}); last lines:\n"
                       + "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-15:]))
    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "repro_check": metadata.version("repro-check"),
        "rscript": exe,
        "session_info": "engine/session_info.txt",
    }
    (run_dir / "environment.json").write_text(json.dumps(env, indent=2))
    return run_dir / "engine"


def simulate(spec: str | Path, out_dir: str | Path) -> Path:
    out_dir = Path(out_dir)
    proc = subprocess.run([rscript(), str(engine_dir() / "simulate.R"), str(spec), str(out_dir)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RunError("simulation failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    return out_dir
