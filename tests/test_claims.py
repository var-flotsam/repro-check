import datetime as dt

import pytest
import yaml

from repro_check import claims as cm

GOOD = {
    "paper": {"doi": "10.1/x", "citation": "X et al."},
    "claims": [
        {"id": "C1", "kind": "qtl_peak", "source": "p.3", "quote": "a QTL at ~34 Mb", "trait": "t",
         "chr": 1, "pos_mb": 34, "founders_high": ["CAST"], "tolerance": {"pos_mb": 4}},
        {"id": "C2", "kind": "qtl_absent", "source": "p.9", "quote": "fell below", "trait": "t",
         "chr": "16", "pos_mb": 90.7},
    ],
}


def write(tmp_path, data, name="claims.yaml"):
    p = tmp_path / name
    p.write_text(yaml.safe_dump(data, sort_keys=False))
    return p


def mutate(**changes):
    import copy
    d = copy.deepcopy(GOOD)
    d["claims"][0].update(changes)
    return d


def test_parses_and_normalises():
    cf = cm.parse(GOOD)
    c1 = cf.claims[0]
    assert c1.chr == "1" and c1.founders_high == ["F"] and c1.tol("pos_mb") == 4.0
    assert c1.tol("lod_abs") == 1.0  # default


@pytest.mark.parametrize("changes, message", [
    ({"kind": "peak"}, "kind must be one of"),
    ({"quote": ""}, "needs 'quote'"),
    ({"founders_high": ["CAST", "BALB"]}, "unknown founder"),
    ({"tolerance": {"pos": 3}}, "unknown tolerance key"),
    ({"tolerance": {"pos_mb": -1}}, ">= 0"),
    ({"founders_low": ["F"]}, "both high and low"),
    ({"surprise": 1}, "unknown field"),
    ({"pos_mb": None}, "needs 'pos_mb'"),
])
def test_rejects_bad_claims(changes, message):
    with pytest.raises(cm.ClaimsError, match=message):
        cm.parse(mutate(**changes))


def test_rejects_duplicate_ids():
    d = mutate()
    d["claims"][1]["id"] = "C1"
    with pytest.raises(cm.ClaimsError, match="duplicate"):
        cm.parse(d)


def test_absent_claim_takes_no_lod():
    d = mutate()
    d["claims"][1]["lod"] = 7.4
    with pytest.raises(cm.ClaimsError, match="no lod"):
        cm.parse(d)


def test_freeze_records_hash_and_load_frozen_accepts(tmp_path):
    p = write(tmp_path, GOOD)
    now = dt.datetime(2026, 10, 23, tzinfo=dt.timezone.utc)
    digest = cm.freeze(p, "Ethan", now=now)
    cf = cm.load_frozen(p)
    assert cf.frozen == {"by": "Ethan", "at": "2026-10-23T00:00:00Z", "sha256": digest}


def test_unfrozen_file_is_refused(tmp_path):
    with pytest.raises(cm.ClaimsError, match="not frozen"):
        cm.load_frozen(write(tmp_path, GOOD))


def test_editing_after_freeze_voids_the_run(tmp_path):
    p = write(tmp_path, GOOD)
    cm.freeze(p, "Ethan")
    data = yaml.safe_load(p.read_text())
    data["claims"][0]["tolerance"]["pos_mb"] = 20  # loosen after the fact
    p.write_text(yaml.safe_dump(data, sort_keys=False))
    with pytest.raises(cm.ClaimsError, match="changed after freezing"):
        cm.load_frozen(p)


def test_cannot_refreeze(tmp_path):
    p = write(tmp_path, GOOD)
    cm.freeze(p, "Ethan")
    with pytest.raises(cm.ClaimsError, match="already frozen"):
        cm.freeze(p, "Ethan")


def test_freeze_needs_a_name(tmp_path):
    with pytest.raises(cm.ClaimsError, match="name"):
        cm.freeze(write(tmp_path, GOOD), "  ")


def test_hash_ignores_key_order_and_frozen_block():
    a = cm.content_hash(GOOD)
    reordered = {"claims": GOOD["claims"], "paper": dict(reversed(list(GOOD["paper"].items())))}
    assert cm.content_hash(reordered) == a
    assert cm.content_hash({**GOOD, "frozen": {"sha256": "x"}}) == a


def test_position_units():
    import copy
    d = copy.deepcopy(GOOD)
    d["paper"]["position_units"] = "cM"
    assert cm.parse(d).claims[0].units == "cM"
    d["paper"]["position_units"] = "bp"
    with pytest.raises(cm.ClaimsError, match="position_units"):
        cm.parse(d)


def test_perm_threshold_needs_alpha():
    import copy
    d = copy.deepcopy(GOOD)
    d["claims"] = [{"id": "P", "kind": "perm_threshold", "source": "s", "quote": "q", "trait": "t", "value": 3.4}]
    with pytest.raises(cm.ClaimsError, match="alpha"):
        cm.parse(d)



def test_package_reads_and_writes_text_as_utf8():
    # On Windows the default is cp1252, which changed the claims hash of a file
    # containing "±" and voided a run. Every text read/write must name UTF-8.
    import re
    from pathlib import Path
    src = Path(__file__).resolve().parents[1] / "src" / "repro_check"
    bad = [f"{f.name}:{n}" for f in src.glob("*.py")
           for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1)
           if re.search(r"\.(read|write)_text\(", line) and 'encoding="utf-8"' not in line]
    assert not bad, bad


def _base():
    return {"paper": {"doi": "x"},
            "claims": [{"id": "A", "kind": "count", "source": "s", "quote": "q", "traits": ["t"], "value": 1}]}


def test_figures_parse_and_validate():
    from repro_check.claims import ClaimsError, parse
    d = _base()
    d["figures"] = [{"id": "F1", "kind": "allele_effects", "source": "Figure 3B", "traits": ["t"], "chr": 1,
                     "region": [20, 50]}]
    cf = parse(d)
    assert cf.figures[0].chr == "1" and cf.figures[0].region == [20.0, 50.0]
    for bad in ({"kind": "allele_effects", "traits": ["t", "u"], "chr": "1"},
                {"kind": "lod_chr", "traits": ["t"]},
                {"kind": "genome_scan", "traits": []},
                {"kind": "genome_scan", "traits": ["t"], "chr": "1"},
                {"kind": "pie", "traits": ["t"]},
                {"kind": "lod_chr", "traits": ["t"], "chr": "1", "region": [5, 1]}):
        d["figures"] = [{"id": "F1", "source": "Fig 1", **bad}]
        with pytest.raises(ClaimsError):
            parse(d)
    d["figures"] = [{"id": "A", "kind": "peak_map", "source": "Fig 1"}]
    with pytest.raises(ClaimsError, match="duplicate"):
        parse(d)


def test_figures_are_hashed_but_old_files_keep_their_hash():
    from repro_check.claims import content_hash
    d = _base()
    h0 = content_hash(d)
    d["figures"] = []
    assert content_hash(d) == h0
    d["figures"] = [{"id": "F1", "kind": "peak_map", "source": "Fig 1"}]
    assert content_hash(d) != h0


def test_figures_only_file_is_allowed():
    from repro_check.claims import ClaimsError, parse
    cf = parse({"paper": {"doi": "x"}, "figures": [{"id": "F1", "kind": "peak_map", "source": "Fig 2B"}]})
    assert cf.claims == [] and len(cf.figures) == 1
    with pytest.raises(ClaimsError):
        parse({"paper": {"doi": "x"}})
