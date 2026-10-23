"""Stage A: synthetic crosses with known answers, through the real R engine.

Skipped when Rscript with qtl2 is not available (see env/).
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from repro_check import cli
from repro_check.fetch import sha256_file
from repro_check.run import RunError, r_env, rscript

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "stage_a"


def _have_qtl2() -> bool:
    try:
        exe = rscript()
    except RunError:
        return False
    return subprocess.run([exe, "-e", "library(qtl2)"], capture_output=True, env=r_env()).returncode == 0


pytestmark = [pytest.mark.r, pytest.mark.skipif(not _have_qtl2(), reason="Rscript with qtl2 not found")]


def _stage(tmp_path, spec=None, claims=None, run_cfg=None):
    work = tmp_path / "work"
    work.mkdir()
    (work / "spec.json").write_text(json.dumps(spec) if spec else (EXAMPLE / "spec.json").read_text())
    shutil.copy(EXAMPLE / "inputs.yaml", work / "inputs.yaml")
    (work / "run.yaml").write_text(yaml.safe_dump(run_cfg) if run_cfg else (EXAMPLE / "run.yaml").read_text())
    (work / "claims.yaml").write_text(yaml.safe_dump(claims) if claims else (EXAMPLE / "claims.yaml").read_text())
    return work


def _pipeline(work: Path) -> dict:
    run = work / "run"
    steps = [
        ["simulate", str(work / "spec.json"), str(work / "sim")],
        ["freeze", str(work / "claims.yaml"), "--by", "test"],
        ["fetch", str(work / "inputs.yaml"), "--run", str(run)],
        ["run", str(work / "run.yaml"), "--run", str(run)],
        ["compare", str(work / "claims.yaml"), "--run", str(run)],
        ["report", str(work / "claims.yaml"), "--run", str(run)],
    ]
    for s in steps:
        assert cli.main(s) == 0, s
    return json.loads((run / "verdicts.json").read_text())


def test_known_answers(tmp_path):
    out = _pipeline(_stage(tmp_path))
    got = {v["claim_id"]: v["verdict"] for v in out["verdicts"]}
    assert got == {
        "S1": "reproduced", "S2": "reproduced", "S3": "reproduced",   # planted QTL
        "S4": "reproduced", "S5": "reproduced",                       # expected nulls
        "S6": "not reproduced", "S7": "not reproduced",               # false claims
    }
    report = (tmp_path / "work" / "run" / "report.md").read_text()
    assert "5 reproduced, 2 not reproduced" in report


def test_simulation_is_deterministic(tmp_path):
    spec = EXAMPLE / "spec.json"
    a, b = tmp_path / "a", tmp_path / "b"
    assert cli.main(["simulate", str(spec), str(a)]) == 0
    assert cli.main(["simulate", str(spec), str(b)]) == 0
    for f in ("pheno.csv", "genoprobs.rds", "map.rds"):
        assert sha256_file(a / f) == sha256_file(b / f), f


def test_null_traits_rarely_cross_the_paper_threshold(tmp_path):
    """20 pure-noise traits on a 4-chromosome genome. With 8-allele scans, LOD 6
    is roughly a 2-5% genome-wide false-positive rate here, so about one of 20
    null traits may cross by chance. Allow at most 2 (10%); more means the
    pipeline inflates LOD. This is also why the report treats an expected null
    as one more claim with a tolerance, not as proof of absence."""
    spec = json.loads((EXAMPLE / "spec.json").read_text())
    spec["seed"] = 7
    spec["traits"] = [{"name": f"null{i:02d}", "noise_sd": 1} for i in range(20)]
    spec["genes"] = []
    claims = {"paper": {"doi": "synthetic/null"}, "claims": [
        {"id": f"N{i:02d}.{chr}", "kind": "qtl_absent", "source": "null sim", "quote": "no QTL",
         "trait": f"null{i:02d}", "chr": str(chr), "pos_mb": 50, "tolerance": {"pos_mb": 50}}
        for i in range(20) for chr in range(1, 5)]}
    run_cfg = yaml.safe_load((EXAMPLE / "run.yaml").read_text())
    run_cfg["traits"] = [{"name": f"null{i:02d}", "transform": "none"} for i in range(20)]
    out = _pipeline(_stage(tmp_path, spec=spec, claims=claims, run_cfg=run_cfg))
    crossed = {v["claim_id"].split(".")[0] for v in out["verdicts"] if v["verdict"] != "reproduced"}
    assert len(crossed) <= 2, sorted(crossed)
