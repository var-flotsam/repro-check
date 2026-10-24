"""Fetch the inputs listed in a manifest and record where each came from.

Manifest (YAML):

    inputs:
      - name: genoprobs
        url: https://example.org/probs.rds      # or a local path / file:// URL
        sha256: 3f5c...                          # optional; refuse on mismatch
        filename: genoprobs.rds                  # optional
        license: CC BY 4.0
        citation: Keller et al. 2018

Downloaded files go to RUN/inputs/. RUN/provenance.json records URL, time,
size and sha256 for every file. Downloaded files are data: nothing here
executes or imports them.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

CHUNK = 1 << 20


class FetchError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def _is_remote(url: str) -> bool:
    return urllib.parse.urlparse(url).scheme in ("http", "https")


def _local_path(url: str, base: Path) -> Path:
    parsed = urllib.parse.urlparse(url)
    p = Path(urllib.parse.unquote(parsed.path)) if parsed.scheme == "file" else Path(url)
    return p if p.is_absolute() else (base / p)


def _download(url: str, dest: Path, timeout: float) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "repro-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, tmp.open("wb") as out:
            shutil.copyfileobj(resp, out, CHUNK)
    except OSError as e:
        tmp.unlink(missing_ok=True)
        raise FetchError(f"could not download {url}: {e}") from e
    tmp.replace(dest)


def load_manifest(path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    inputs = data.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        raise FetchError(f"{path}: needs a non-empty 'inputs' list")
    names = set()
    for i, item in enumerate(inputs):
        if not isinstance(item, dict) or not item.get("name") or not item.get("url"):
            raise FetchError(f"{path}: input #{i + 1} needs 'name' and 'url'")
        if item["name"] in names:
            raise FetchError(f"{path}: duplicate input name {item['name']!r}")
        names.add(item["name"])
    return inputs


def fetch(manifest: str | Path, run_dir: str | Path, timeout: float = 600.0) -> dict[str, Any]:
    """Fetch every input; returns the provenance record (also written to disk)."""
    manifest = Path(manifest)
    run_dir = Path(run_dir)
    dest_dir = run_dir / "inputs"
    dest_dir.mkdir(parents=True, exist_ok=True)
    records = {}
    for item in load_manifest(manifest):
        url = item["url"]
        name = item["name"]
        filename = item.get("filename") or Path(urllib.parse.urlparse(url).path).name or name
        dest = dest_dir / filename
        if _is_remote(url):
            _download(url, dest, timeout)
        else:
            src = _local_path(url, manifest.parent)
            if not src.is_file():
                raise FetchError(f"input {name!r}: local file {src} not found")
            shutil.copyfile(src, dest)
        digest = sha256_file(dest)
        expected = item.get("sha256")
        if expected and digest != expected.lower():
            dest.unlink()
            raise FetchError(f"input {name!r}: sha256 mismatch for {url}\n"
                             f"  expected {expected}\n  got      {digest}\n"
                             "The file was deleted. If the source changed on purpose, update the "
                             "manifest and say so in the report.")
        records[name] = {
            "url": url,
            "path": str(dest.relative_to(run_dir)),
            "retrieved_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "bytes": dest.stat().st_size,
            "sha256": digest,
            "sha256_expected": expected,
            "license": item.get("license"),
            "citation": item.get("citation"),
        }
    prov = {"manifest": str(manifest), "manifest_sha256": sha256_file(manifest), "inputs": records}
    (run_dir / "provenance.json").write_text(json.dumps(prov, indent=2), encoding="utf-8")
    return prov
