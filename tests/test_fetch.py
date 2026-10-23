import http.server
import json
import threading

import pytest
import yaml

from repro_check import fetch as fm


def manifest(tmp_path, items):
    p = tmp_path / "inputs.yaml"
    p.write_text(yaml.safe_dump({"inputs": items}))
    return p


@pytest.fixture
def data_file(tmp_path):
    d = tmp_path / "src"
    d.mkdir()
    f = d / "pheno.csv"
    f.write_text("id,x\na,1\n")
    return f


def test_local_copy_records_provenance(tmp_path, data_file):
    m = manifest(tmp_path, [{"name": "pheno", "url": "src/pheno.csv", "license": "CC0"}])
    prov = fm.fetch(m, tmp_path / "run")
    rec = prov["inputs"]["pheno"]
    assert rec["sha256"] == fm.sha256_file(data_file)
    assert rec["bytes"] == data_file.stat().st_size and rec["license"] == "CC0"
    assert json.loads((tmp_path / "run" / "provenance.json").read_text()) == prov


def test_checksum_mismatch_refuses_and_deletes(tmp_path, data_file):
    m = manifest(tmp_path, [{"name": "pheno", "url": "src/pheno.csv", "sha256": "0" * 64}])
    with pytest.raises(fm.FetchError, match="sha256 mismatch"):
        fm.fetch(m, tmp_path / "run")
    assert not (tmp_path / "run" / "inputs" / "pheno.csv").exists()


def test_matching_checksum_passes(tmp_path, data_file):
    m = manifest(tmp_path, [{"name": "pheno", "url": "src/pheno.csv", "sha256": fm.sha256_file(data_file)}])
    assert fm.fetch(m, tmp_path / "run")["inputs"]["pheno"]["sha256_expected"]


def test_missing_local_file(tmp_path):
    with pytest.raises(fm.FetchError, match="not found"):
        fm.fetch(manifest(tmp_path, [{"name": "x", "url": "nope.rds"}]), tmp_path / "run")


def test_duplicate_names(tmp_path, data_file):
    items = [{"name": "p", "url": "src/pheno.csv"}] * 2
    with pytest.raises(fm.FetchError, match="duplicate"):
        fm.fetch(manifest(tmp_path, items), tmp_path / "run")


def test_http_download(tmp_path, data_file):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(data_file.parent), **k)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        url = f"http://127.0.0.1:{srv.server_address[1]}/pheno.csv"
        prov = fm.fetch(manifest(tmp_path, [{"name": "pheno", "url": url}]), tmp_path / "run")
    finally:
        srv.shutdown()
    assert prov["inputs"]["pheno"]["sha256"] == fm.sha256_file(data_file)
