import json

import pytest
import yaml

from helpers import claim, peak, results
from repro_check import cli
from repro_check.claims import ClaimsFile
from repro_check.compare import compare_all
from repro_check.report import render

ACCUSING = ("error", "mistake", "wrong", "fault", "flawed", "fraud", "incorrect")


def test_report_restates_computed_verdicts(tmp_path):
    cs = [claim(lod=7.4, founders_high=["F"]), claim(id="C2", kind="qtl_absent", chr="2")]
    vs = compare_all(cs, results([peak(lod=7.9)]))
    cf = ClaimsFile(paper={"doi": "10.1/x"}, claims=cs, frozen={"by": "E", "at": "t", "sha256": "abc"})
    text = render(cf, vs, tmp_path)
    assert "| C1 |" in text and "**reproduced**" in text
    assert "sha256 `abc`" in text
    lowered = text.lower()
    assert not any(w in lowered for w in ACCUSING)


def _frozen_claims(tmp_path):
    p = tmp_path / "claims.yaml"
    p.write_text(yaml.safe_dump({"paper": {"doi": "10.1/x"}, "claims": [
        {"id": "C1", "kind": "qtl_absent", "source": "s", "quote": "q", "trait": "t", "chr": "1", "pos_mb": 10}]}))
    return p


def test_compare_refuses_unfrozen_claims(tmp_path, capsys):
    p = _frozen_claims(tmp_path)
    assert cli.main(["compare", str(p), "--run", str(tmp_path)]) == 2
    assert "not frozen" in capsys.readouterr().err


def test_report_refuses_verdicts_from_other_claims(tmp_path, capsys):
    p = _frozen_claims(tmp_path)
    assert cli.main(["freeze", str(p), "--by", "E"]) == 0
    (tmp_path / "verdicts.json").write_text(json.dumps({"claims_sha256": "other", "verdicts": []}))
    assert cli.main(["report", str(p), "--run", str(tmp_path)]) == 2
    assert "different claims" in capsys.readouterr().err
