"""Read an engine run: results.json plus the gzipped LOD profile."""

from __future__ import annotations

import csv
import gzip
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Peak:
    trait: str
    chr: str
    pos: float
    lod: float
    ci_lo: float
    ci_hi: float
    marker: str
    coef: dict[str, float]


@dataclass
class Profile:
    """LOD at every marker; `lod[trait]` is aligned with `chr` and `pos`."""

    chr: list[str]
    pos: list[float]
    lod: dict[str, list[float]]

    def window_max(self, trait: str, chr: str, lo: float, hi: float) -> tuple[float, float] | None:
        """Largest LOD and its position for `trait` on `chr` within [lo, hi]."""
        best: tuple[float, float] | None = None
        values = self.lod[trait]
        for c, p, v in zip(self.chr, self.pos, values):
            if c == chr and lo <= p <= hi and v == v:  # v == v skips NaN
                if best is None or v > best[0]:
                    best = (v, p)
        return best


@dataclass
class RunResults:
    traits: list[str]
    n_mapped: dict[str, int]
    peaks: list[Peak]
    profile: Profile
    report_threshold: float
    engine: dict[str, Any]
    permutation_thresholds: dict[str, Any] | None
    notes: dict[str, str] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def peaks_for(self, trait: str, chr: str | None = None) -> list[Peak]:
        return [p for p in self.peaks if p.trait == trait and (chr is None or p.chr == chr)]


def _num(x: str) -> float:
    return float("nan") if x in ("", "NA", "NaN") else float(x)


def read_profile(path: Path) -> Profile:
    with gzip.open(path, "rt", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        if header[:3] != ["marker", "chr", "pos"]:
            raise ValueError(f"{path}: expected columns marker, chr, pos first; got {header[:3]}")
        traits = header[3:]
        chrs: list[str] = []
        pos: list[float] = []
        lod: dict[str, list[float]] = {t: [] for t in traits}
        for row in reader:
            chrs.append(row[1])
            pos.append(float(row[2]))
            for t, v in zip(traits, row[3:]):
                lod[t].append(_num(v))
    return Profile(chr=chrs, pos=pos, lod=lod)


def load(run_dir: str | Path) -> RunResults:
    run_dir = Path(run_dir)
    raw = json.loads((run_dir / "results.json").read_text())
    profile = read_profile(run_dir / raw.get("profile", "lod_profile.csv.gz"))
    peaks = [
        Peak(trait=p["trait"], chr=str(p["chr"]), pos=float(p["pos"]), lod=float(p["lod"]),
             ci_lo=float(p["ci_lo"]), ci_hi=float(p["ci_hi"]), marker=p["marker"],
             coef={k: float(v) for k, v in p["coef"].items()})
        for p in raw.get("peaks") or []
    ]
    cfg = raw.get("config") or {}
    return RunResults(
        traits=list(profile.lod),
        n_mapped={k: int(v) for k, v in (raw.get("n_mapped") or {}).items()},
        peaks=peaks,
        profile=profile,
        report_threshold=float(cfg.get("report_threshold", 3.0)),
        engine=raw.get("engine") or {},
        permutation_thresholds=raw.get("permutation_thresholds"),
        notes=raw.get("notes") or {},
        raw=raw,
    )
