"""Claims file: load, validate, freeze and verify.

A claims file lists what a paper says, each with a tolerance chosen before
any data is fetched. `freeze` records who confirmed the claims and a sha256
of their canonical form; every later step refuses to run if the claims no
longer match that hash.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .founders import FOUNDER_CODES, normalise_founders

KINDS = ("qtl_peak", "qtl_absent", "effect_pattern", "count")

DEFAULT_TOLERANCE = {
    # Peak position: DO peaks are usually resolved to a few Mb, and genoprobs
    # builds and marker sets can move them by about that much.
    "pos_mb": 5.0,
    # LOD: genoprobs version, kinship and missing-data handling shift LOD by
    # around 1; for large peaks a relative band is fairer.
    "lod_abs": 1.0,
    "lod_rel": 0.15,
    "lod_rel_above": 10.0,
    # Peak must clear the paper's own threshold to count as found.
    "threshold_lod": 6.0,
    # Count claims depend on peak-calling rules papers rarely give.
    "count_rel": 0.20,
}


class ClaimsError(ValueError):
    """The claims file is malformed, or was changed after freezing."""


@dataclass
class Claim:
    id: str
    kind: str
    source: str
    quote: str
    trait: str | None = None
    traits: list[str] = field(default_factory=list)
    chr: str | None = None
    pos_mb: float | None = None
    pos_reported_precision_mb: float = 0.0
    lod: float | None = None
    value: float | None = None
    founders_high: list[str] = field(default_factory=list)
    founders_low: list[str] = field(default_factory=list)
    tolerance: dict[str, float] = field(default_factory=dict)
    notes: str = ""

    def tol(self, key: str) -> float:
        return float(self.tolerance.get(key, DEFAULT_TOLERANCE[key]))


@dataclass
class ClaimsFile:
    paper: dict[str, Any]
    claims: list[Claim]
    frozen: dict[str, Any] | None
    path: Path | None = None

    def by_id(self) -> dict[str, Claim]:
        return {c.id: c for c in self.claims}


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ClaimsError(msg)


def _founders(names: Any, where: str) -> list[str]:
    _require(names is None or isinstance(names, list), f"{where}: founders must be a list")
    try:
        return normalise_founders(names or [], where)
    except ValueError as e:
        raise ClaimsError(str(e)) from e


def _parse_claim(raw: dict[str, Any], index: int) -> Claim:
    where = f"claim #{index + 1}"
    _require(isinstance(raw, dict), f"{where}: must be a mapping")
    cid = raw.get("id")
    _require(isinstance(cid, str) and cid, f"{where}: needs a string 'id'")
    where = f"claim {cid}"
    kind = raw.get("kind")
    _require(kind in KINDS, f"{where}: kind must be one of {', '.join(KINDS)}, got {kind!r}")
    for key in ("source", "quote"):
        _require(isinstance(raw.get(key), str) and raw[key].strip(),
                 f"{where}: needs '{key}' (where in the paper, and the words it uses)")
    known = set(Claim.__dataclass_fields__)
    unknown = set(raw) - known
    _require(not unknown, f"{where}: unknown field(s) {sorted(unknown)}")
    tol = raw.get("tolerance") or {}
    bad_tol = set(tol) - set(DEFAULT_TOLERANCE)
    _require(not bad_tol, f"{where}: unknown tolerance key(s) {sorted(bad_tol)}; "
             f"allowed: {sorted(DEFAULT_TOLERANCE)}")
    for k, v in tol.items():
        _require(isinstance(v, (int, float)) and v >= 0, f"{where}: tolerance.{k} must be a number >= 0")

    claim = Claim(
        id=cid, kind=kind, source=raw["source"], quote=raw["quote"],
        trait=raw.get("trait"), traits=list(raw.get("traits") or []),
        chr=None if raw.get("chr") is None else str(raw["chr"]),
        pos_mb=None if raw.get("pos_mb") is None else float(raw["pos_mb"]),
        pos_reported_precision_mb=float(raw.get("pos_reported_precision_mb") or 0.0),
        lod=None if raw.get("lod") is None else float(raw["lod"]),
        value=None if raw.get("value") is None else float(raw["value"]),
        founders_high=_founders(raw.get("founders_high"), where),
        founders_low=_founders(raw.get("founders_low"), where),
        tolerance={k: float(v) for k, v in tol.items()},
        notes=raw.get("notes") or "",
    )

    if kind in ("qtl_peak", "qtl_absent", "effect_pattern"):
        _require(bool(claim.trait), f"{where}: {kind} needs 'trait'")
        _require(claim.chr is not None, f"{where}: {kind} needs 'chr'")
        _require(claim.pos_mb is not None, f"{where}: {kind} needs 'pos_mb'")
    if kind == "qtl_absent":
        _require(claim.lod is None and not claim.founders_high and not claim.founders_low,
                 f"{where}: qtl_absent takes no lod or founders")
    if kind == "effect_pattern":
        _require(bool(claim.founders_high or claim.founders_low),
                 f"{where}: effect_pattern needs founders_high and/or founders_low")
    if kind == "count":
        _require(bool(claim.traits), f"{where}: count needs 'traits' (list)")
        _require(claim.value is not None, f"{where}: count needs 'value'")
    overlap = set(claim.founders_high) & set(claim.founders_low)
    _require(not overlap, f"{where}: founder(s) {sorted(overlap)} listed as both high and low")
    _require(len(claim.founders_high) + len(claim.founders_low) <= len(FOUNDER_CODES),
             f"{where}: too many founders")
    return claim


def parse(data: dict[str, Any], path: Path | None = None) -> ClaimsFile:
    _require(isinstance(data, dict), "claims file must be a mapping")
    paper = data.get("paper")
    _require(isinstance(paper, dict) and paper.get("doi"), "claims file needs paper.doi")
    raw_claims = data.get("claims")
    _require(isinstance(raw_claims, list) and raw_claims, "claims file needs a non-empty 'claims' list")
    claims = [_parse_claim(c, i) for i, c in enumerate(raw_claims)]
    ids = [c.id for c in claims]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    _require(not dupes, f"duplicate claim id(s): {dupes}")
    return ClaimsFile(paper=paper, claims=claims, frozen=data.get("frozen"), path=path)


def load(path: str | Path) -> ClaimsFile:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise ClaimsError(f"{path}: not valid YAML: {e}") from e
    return parse(data, path)


def content_hash(data: dict[str, Any]) -> str:
    """sha256 of the paper and claims sections in canonical JSON.

    The `frozen` block is excluded so that recording the hash does not change it.
    """
    canonical = json.dumps({"paper": data.get("paper"), "claims": data.get("claims")},
                           sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def freeze(path: str | Path, by: str, now: dt.datetime | None = None) -> str:
    """Validate, then write the frozen block into the file. Returns the hash."""
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    parse(data, path)
    if data.get("frozen"):
        raise ClaimsError(f"{path}: already frozen at {data['frozen'].get('at')}; "
                          "start a new claims file instead of re-freezing")
    _require(bool(by.strip()), "freeze needs the name of the person who confirmed the claims")
    digest = content_hash(data)
    now = now or dt.datetime.now(dt.timezone.utc)
    data["frozen"] = {"by": by, "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "sha256": digest}
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    return digest


def load_frozen(path: str | Path) -> ClaimsFile:
    """Load a claims file and check it is frozen and unchanged since."""
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    cf = parse(data, path)
    frozen = data.get("frozen")
    if not frozen or not frozen.get("sha256"):
        raise ClaimsError(f"{path}: not frozen; run `repro-check freeze` after the claims are confirmed")
    actual = content_hash(data)
    if actual != frozen["sha256"]:
        raise ClaimsError(f"{path}: claims changed after freezing "
                          f"(frozen {frozen['sha256'][:12]}, now {actual[:12]}); this run is void")
    return cf
