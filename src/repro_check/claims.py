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

KINDS = ("qtl_peak", "qtl_absent", "effect_pattern", "count", "perm_threshold")
FIGURE_KINDS = ("genome_scan", "lod_chr", "allele_effects", "peak_map")
UNITS = ("Mb", "cM")

DEFAULT_TOLERANCE = {
    # Peak position: DO peaks are usually resolved to a few Mb, and genoprobs
    # builds and marker sets can move them by about that much.
    "pos_mb": 5.0,
    # 1: a claimed position inside the observed support interval also passes.
    # Set 0 when rerunning the authors' own data and software, where the
    # position should match to the marker.
    "pos_ci": 1.0,
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
    alpha: float | None = None
    founders_high: list[str] = field(default_factory=list)
    founders_low: list[str] = field(default_factory=list)
    tolerance: dict[str, float] = field(default_factory=dict)
    notes: str = ""
    units: str = "Mb"

    def tol(self, key: str) -> float:
        return float(self.tolerance.get(key, DEFAULT_TOLERANCE[key]))


@dataclass
class Figure:
    """A paper figure to redraw from this run. Figures never get a verdict."""
    id: str
    kind: str
    source: str
    traits: list[str] = field(default_factory=list)
    chr: str | None = None
    region: list[float] | None = None
    thresholds: list[float] = field(default_factory=list)
    url: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


@dataclass
class ClaimsFile:
    paper: dict[str, Any]
    claims: list[Claim]
    frozen: dict[str, Any] | None
    path: Path | None = None
    figures: list[Figure] = field(default_factory=list)

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


def _parse_claim(raw: dict[str, Any], index: int, units: str = "Mb") -> Claim:
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
    known = set(Claim.__dataclass_fields__) - {"units"}
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
        alpha=None if raw.get("alpha") is None else float(raw["alpha"]),
        founders_high=_founders(raw.get("founders_high"), where),
        founders_low=_founders(raw.get("founders_low"), where),
        tolerance={k: float(v) for k, v in tol.items()},
        notes=raw.get("notes") or "",
        units=units,
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
    if kind == "perm_threshold":
        _require(bool(claim.trait), f"{where}: perm_threshold needs 'trait'")
        _require(claim.value is not None, f"{where}: perm_threshold needs 'value' (the LOD threshold)")
        _require(claim.alpha is not None and 0 < claim.alpha < 1, f"{where}: perm_threshold needs 'alpha' in (0, 1)")
    if kind == "count":
        _require(bool(claim.traits), f"{where}: count needs 'traits' (list)")
        _require(claim.value is not None, f"{where}: count needs 'value'")
    overlap = set(claim.founders_high) & set(claim.founders_low)
    _require(not overlap, f"{where}: founder(s) {sorted(overlap)} listed as both high and low")
    _require(len(claim.founders_high) + len(claim.founders_low) <= len(FOUNDER_CODES),
             f"{where}: too many founders")
    return claim


def _parse_figure(raw: dict[str, Any], index: int) -> Figure:
    where = f"figure #{index + 1}"
    _require(isinstance(raw, dict), f"{where}: must be a mapping")
    fid = raw.get("id")
    _require(isinstance(fid, str) and fid, f"{where}: needs a string 'id'")
    where = f"figure {fid}"
    unknown = set(raw) - set(Figure.__dataclass_fields__)
    _require(not unknown, f"{where}: unknown field(s) {sorted(unknown)}")
    kind = raw.get("kind")
    _require(kind in FIGURE_KINDS, f"{where}: kind must be one of {', '.join(FIGURE_KINDS)}, got {kind!r}")
    _require(isinstance(raw.get("source"), str) and raw["source"].strip(),
             f"{where}: needs 'source' (the paper's figure and panel, e.g. 'Figure 2A')")
    traits = raw.get("traits") or []
    _require(isinstance(traits, list) and all(isinstance(t, str) for t in traits),
             f"{where}: traits must be a list of trait names")
    region = raw.get("region")
    if region is not None:
        _require(isinstance(region, list) and len(region) == 2 and all(isinstance(x, (int, float)) for x in region)
                 and region[0] < region[1], f"{where}: region must be [start, end] with start < end")
        region = [float(x) for x in region]
    fig = Figure(id=fid, kind=kind, source=raw["source"], traits=list(traits),
                 chr=None if raw.get("chr") is None else str(raw["chr"]), region=region,
                 thresholds=[float(x) for x in raw.get("thresholds") or []],
                 url=raw.get("url") or "", notes=raw.get("notes") or "")
    if kind in ("genome_scan", "lod_chr"):
        _require(bool(fig.traits), f"{where}: {kind} needs at least one trait")
    if kind in ("lod_chr", "allele_effects"):
        _require(fig.chr is not None, f"{where}: {kind} needs 'chr'")
    if kind == "allele_effects":
        _require(len(fig.traits) == 1, f"{where}: allele_effects takes exactly one trait")
    if kind == "genome_scan":
        _require(region is None and fig.chr is None, f"{where}: genome_scan covers every chromosome")
    return fig


def parse(data: dict[str, Any], path: Path | None = None) -> ClaimsFile:
    _require(isinstance(data, dict), "claims file must be a mapping")
    paper = data.get("paper")
    _require(isinstance(paper, dict) and paper.get("doi"), "claims file needs paper.doi")
    raw_claims = data.get("claims") or []
    _require(isinstance(raw_claims, list), "'claims' must be a list")
    _require(bool(raw_claims) or bool(data.get("figures")),
             "claims file needs a non-empty 'claims' list (or, for a figures-only file, 'figures')")
    units = paper.get("position_units", "Mb")
    _require(units in UNITS, f"paper.position_units must be one of {UNITS}, got {units!r}")
    claims = [_parse_claim(c, i, units) for i, c in enumerate(raw_claims)]
    ids = [c.id for c in claims]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    _require(not dupes, f"duplicate claim id(s): {dupes}")
    raw_figures = data.get("figures") or []
    _require(isinstance(raw_figures, list), "'figures' must be a list")
    figures = [_parse_figure(f, i) for i, f in enumerate(raw_figures)]
    fids = [f.id for f in figures]
    dupes = sorted({i for i in fids if fids.count(i) > 1} | (set(fids) & set(ids)))
    _require(not dupes, f"duplicate figure id(s) or ids shared with claims: {dupes}")
    return ClaimsFile(paper=paper, claims=claims, frozen=data.get("frozen"), path=path, figures=figures)


def load(path: str | Path) -> ClaimsFile:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ClaimsError(f"{path}: not valid YAML: {e}") from e
    return parse(data, path)


def content_hash(data: dict[str, Any]) -> str:
    """sha256 of the paper and claims sections in canonical JSON.

    The `frozen` block is excluded so that recording the hash does not change it.
    `figures` is included when present, so files without it hash as before.
    """
    hashed = {"paper": data.get("paper"), "claims": data.get("claims")}
    if data.get("figures"):
        hashed["figures"] = data["figures"]
    canonical = json.dumps(hashed,
                           sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def freeze(path: str | Path, by: str, now: dt.datetime | None = None) -> str:
    """Validate, then write the frozen block into the file. Returns the hash."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    parse(data, path)
    if data.get("frozen"):
        raise ClaimsError(f"{path}: already frozen at {data['frozen'].get('at')}; "
                          "start a new claims file instead of re-freezing")
    _require(bool(by.strip()), "freeze needs the name of the person who confirmed the claims")
    digest = content_hash(data)
    now = now or dt.datetime.now(dt.timezone.utc)
    data["frozen"] = {"by": by, "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "sha256": digest}
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return digest


def load_frozen(path: str | Path) -> ClaimsFile:
    """Load a claims file and check it is frozen and unchanged since."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    cf = parse(data, path)
    frozen = data.get("frozen")
    if not frozen or not frozen.get("sha256"):
        raise ClaimsError(f"{path}: not frozen; run `repro-check freeze` after the claims are confirmed")
    actual = content_hash(data)
    if actual != frozen["sha256"]:
        raise ClaimsError(f"{path}: claims changed after freezing "
                          f"(frozen {frozen['sha256'][:12]}, now {actual[:12]}); this run is void")
    return cf
