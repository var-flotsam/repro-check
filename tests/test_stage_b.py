"""Stage B: R/qtl2 user-guide examples, fetched from GitHub at pinned commits.

Needs Rscript with qtl2 and network access to raw.githubusercontent.com.
Permutation claims are left out here: their verdicts are recorded in
docs/results/ and depend on the permutation draw.
"""

import json
import shutil
import urllib.request
from pathlib import Path

import pytest
import yaml

from repro_check import cli
from test_stage_a import _have_qtl2

ROOT = Path(__file__).resolve().parents[1]


def _online() -> bool:
    try:
        urllib.request.urlopen("https://raw.githubusercontent.com", timeout=10)
        return True
    except OSError as e:
        return getattr(e, "code", None) is not None  # an HTTP error still means we reached it


pytestmark = [pytest.mark.r, pytest.mark.network,
              pytest.mark.skipif(not _have_qtl2(), reason="Rscript with qtl2 not found"),
              pytest.mark.skipif(not _online(), reason="no network")]


def _run(tmp_path, example, drop_perm=True):
    src = ROOT / "examples" / example
    work = tmp_path / example
    work.mkdir()
    claims = yaml.safe_load((src / "claims.yaml").read_text())
    claims["claims"] = [c for c in claims["claims"] if not (drop_perm and c["kind"] == "perm_threshold")]
    (work / "claims.yaml").write_text(yaml.safe_dump(claims, sort_keys=False))
    cfg = yaml.safe_load((src / "run.yaml").read_text())
    cfg["n_perm"] = 0
    (work / "run.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
    shutil.copy(src / "inputs.yaml", work / "inputs.yaml")
    run = work / "run"
    for step in (["freeze", str(work / "claims.yaml"), "--by", "test"],
                 ["fetch", str(work / "inputs.yaml"), "--run", str(run)],
                 ["run", str(work / "run.yaml"), "--run", str(run)],
                 ["compare", str(work / "claims.yaml"), "--run", str(run)]):
        assert cli.main(step) == 0, step
    return {v["claim_id"]: v["verdict"] for v in json.loads((run / "verdicts.json").read_text())["verdicts"]}


def test_iron_user_guide_peaks(tmp_path):
    got = _run(tmp_path, "stage_b_iron")
    assert got == {f"B{i}": "reproduced" for i in range(1, 8)}


def test_doex_user_guide_peak(tmp_path):
    assert _run(tmp_path, "stage_b_doex") == {"D1": "reproduced"}
