"""Builders for hand-made engine results, so verdict logic is tested without R."""

from __future__ import annotations

from repro_check.claims import Claim
from repro_check.founders import FOUNDER_CODES
from repro_check.results import Peak, Profile, RunResults


def coef(high: str | None = None, low: str | None = None, order: str | None = None) -> dict[str, float]:
    """Founder effects. `order` like "FABCDEGH" gives a strict ranking, high to low."""
    if order:
        return {c: float(len(order) - i) for i, c in enumerate(order)}
    out = {c: 0.0 for c in FOUNDER_CODES}
    if high:
        out[high] = 1.0
    if low:
        out[low] = -1.0
    return out


def peak(trait="t", chr="1", pos=34.0, lod=8.0, ci=None, c=None) -> Peak:
    lo, hi = ci if ci else (pos - 1, pos + 1)
    return Peak(trait=trait, chr=chr, pos=pos, lod=lod, ci_lo=lo, ci_hi=hi, marker=f"m{pos}",
                coef=c or coef(high="F"))


def results(peaks=(), profile=None, traits=("t",), report_threshold=3.0) -> RunResults:
    if profile is None:
        # Flat LOD 1 everywhere on chr 1-3, 0-100 Mb in 1 Mb steps, raised at each peak.
        chrs, pos = [], []
        for ch in ("1", "2", "3"):
            for p in range(0, 101):
                chrs.append(ch)
                pos.append(float(p))
        lod = {t: [1.0] * len(pos) for t in traits}
        for pk in peaks:
            for i, (ch, p) in enumerate(zip(chrs, pos)):
                if ch == pk.chr and p == round(pk.pos):
                    lod[pk.trait][i] = pk.lod
        profile = Profile(chr=chrs, pos=pos, lod=lod)
    return RunResults(traits=list(profile.lod), n_mapped={t: 100 for t in profile.lod}, peaks=list(peaks),
                      profile=profile, report_threshold=report_threshold, engine={},
                      permutation_thresholds=None)


def claim(**kw) -> Claim:
    base = dict(id="C1", kind="qtl_peak", source="p.1", quote="q", trait="t", chr="1", pos_mb=34.0)
    base.update(kw)
    return Claim(**base)
