import json

import pytest

from repro_check.run import RunError, build_engine_config


def _run_dir(tmp_path):
    (tmp_path / "inputs").mkdir()
    (tmp_path / "inputs" / "probs.rds").write_bytes(b"x")
    (tmp_path / "provenance.json").write_text(json.dumps({"inputs": {"probs": {"path": "inputs/probs.rds"}}}))
    return tmp_path


def test_resolves_input_and_run_paths(tmp_path):
    run = _run_dir(tmp_path)
    (run / "derived").mkdir()
    (run / "derived" / "pheno.csv").write_text("id\n")
    cfg = {"genoprobs": "input:probs", "map": "input:probs", "pheno": "run:derived/pheno.csv",
           "traits": [{"name": "t"}], "seed": 1}
    out = build_engine_config(cfg, run)
    assert out["genoprobs"] == str((run / "inputs" / "probs.rds").resolve())
    assert out["pheno"] == str((run / "derived" / "pheno.csv").resolve())


def test_missing_run_path_is_an_error(tmp_path):
    run = _run_dir(tmp_path)
    cfg = {"genoprobs": "input:probs", "map": "input:probs", "pheno": "run:derived/pheno.csv",
           "traits": [{"name": "t"}], "seed": 1}
    with pytest.raises(RunError, match="does not exist"):
        build_engine_config(cfg, run)
