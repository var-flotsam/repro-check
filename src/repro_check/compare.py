"""Turn claims plus engine results into verdicts.

This module is the only place a verdict is decided. Every function is pure:
the same claim and results always give the same verdict, and every verdict
carries the numbers and tolerances behind it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .claims import Claim
from .founders import FOUNDER_CODES, FOUNDERS
from .results import Peak, RunResults

REPRODUCED = "reproduced"
PARTLY = "partly reproduced"
NOT_REPRODUCED = "not reproduced"
NOT_CHECKABLE = "not checkable"
VERDICTS = (REPRODUCED, PARTLY, NOT_REPRODUCED, NOT_CHECKABLE)


@dataclass
class Check:
    name: str
    passed: bool
    claimed: Any
    observed: Any
    tolerance: str
    detail: str = ""


@dataclass
class Verdict:
    claim_id: str
    kind: str
    verdict: str
    checks: list[Check] = field(default_factory=list)
    observed: dict[str, Any] = field(default_factory=dict)
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _fmt(x: float | None, nd: int = 2) -> str:
    return "—" if x is None else f"{x:.{nd}f}"


def position_half_width(claim: Claim) -> float:
    """Allowed distance from the claimed position: the stated tolerance or the
    paper's own rounding, whichever is wider."""
    return max(claim.tol("pos_mb"), claim.pos_reported_precision_mb)


def lod_allowance(claim: Claim) -> float:
    assert claim.lod is not None
    if claim.lod > claim.tol("lod_rel_above"):
        return claim.tol("lod_rel") * claim.lod
    return claim.tol("lod_abs")


def _position_ok(claim: Claim, peak: Peak, half: float) -> bool:
    assert claim.pos_mb is not None
    if abs(peak.pos - claim.pos_mb) <= half:
        return True
    return claim.tol("pos_ci") > 0 and peak.ci_lo <= claim.pos_mb <= peak.ci_hi


def _ranked(coef: dict[str, float]) -> list[str]:
    """Founder codes from highest to lowest effect (ties broken by code)."""
    return sorted(FOUNDER_CODES, key=lambda c: (-coef[c], c))


def pattern_check(claim: Claim, coef: dict[str, float]) -> Check:
    """One listed founder must be the extreme; several must all be in that half."""
    if not set(FOUNDER_CODES) <= set(coef):
        return Check("founder pattern", False, "founder pattern", "no founder effects at this peak",
                     "needs the eight DO/CC founder effects A-H",
                     f"effects available: {', '.join(sorted(coef))}")
    ranked = _ranked(coef)
    half = len(ranked) // 2
    problems = []
    if claim.founders_high:
        if len(claim.founders_high) == 1:
            if ranked[0] != claim.founders_high[0]:
                problems.append(f"highest is {FOUNDERS[ranked[0]]}, not {FOUNDERS[claim.founders_high[0]]}")
        else:
            out = [c for c in claim.founders_high if c not in ranked[:half]]
            if out:
                problems.append("not in upper half: " + ", ".join(FOUNDERS[c] for c in out))
    if claim.founders_low:
        if len(claim.founders_low) == 1:
            if ranked[-1] != claim.founders_low[0]:
                problems.append(f"lowest is {FOUNDERS[ranked[-1]]}, not {FOUNDERS[claim.founders_low[0]]}")
        else:
            out = [c for c in claim.founders_low if c not in ranked[half:]]
            if out:
                problems.append("not in lower half: " + ", ".join(FOUNDERS[c] for c in out))
    order = " > ".join(FOUNDERS[c] for c in ranked)
    claimed = "high: " + (", ".join(FOUNDERS[c] for c in claim.founders_high) or "—") + \
              "; low: " + (", ".join(FOUNDERS[c] for c in claim.founders_low) or "—")
    return Check(
        name="founder pattern", passed=not problems, claimed=claimed, observed=order,
        tolerance="a single listed founder must be the extreme; several must all fall in that half",
        detail="; ".join(problems),
    )


def _find_peak(claim: Claim, results: RunResults) -> tuple[Peak | None, list[Check], dict[str, Any]]:
    """Locate the peak a claim refers to; returns it with position and threshold checks."""
    assert claim.trait and claim.chr is not None and claim.pos_mb is not None
    half = position_half_width(claim)
    threshold = claim.tol("threshold_lod")
    lo, hi = claim.pos_mb - half, claim.pos_mb + half
    candidates = [p for p in results.peaks_for(claim.trait, claim.chr) if _position_ok(claim, p, half)]
    window = results.profile.window_max(claim.trait, claim.chr, lo, hi)
    observed: dict[str, Any] = {"window_mb": [lo, hi]}
    if window:
        observed["window_max_lod"], observed["window_max_pos"] = window
    pos_tol = f"±{half:g} {claim.units}" + (
        ", or claimed position inside the observed support interval" if claim.tol("pos_ci") > 0 else "")
    if not candidates:
        checks = [
            Check("position", False, f"chr {claim.chr} {claim.pos_mb:g} {claim.units}", "no called peak in window",
                  pos_tol, f"max LOD in window {_fmt(window[0] if window else None)}"),
            Check("threshold", False, f"LOD ≥ {threshold:g}", _fmt(window[0] if window else None),
                  "paper's threshold"),
        ]
        return None, checks, observed
    peak = max(candidates, key=lambda p: p.lod)
    observed.update({"chr": peak.chr, "pos": peak.pos, "lod": peak.lod,
                     "ci": [peak.ci_lo, peak.ci_hi], "marker": peak.marker, "coef": peak.coef})
    checks = [
        Check("position", True, f"chr {claim.chr} {claim.pos_mb:g} {claim.units}",
              f"chr {peak.chr} {peak.pos:g} {claim.units} (support {peak.ci_lo:g}–{peak.ci_hi:g})", pos_tol),
        Check("threshold", peak.lod >= threshold, f"LOD ≥ {threshold:g}", _fmt(peak.lod),
              "paper's threshold"),
    ]
    return peak, checks, observed


def _check_peak(claim: Claim, results: RunResults) -> Verdict:
    peak, checks, observed = _find_peak(claim, results)
    found = all(c.passed for c in checks)
    if peak is not None and claim.lod is not None:
        allow = lod_allowance(claim)
        checks.append(Check("LOD", abs(peak.lod - claim.lod) <= allow, _fmt(claim.lod), _fmt(peak.lod),
                            f"±{allow:.2f}", f"difference {peak.lod - claim.lod:+.2f}"))
    if peak is not None and (claim.founders_high or claim.founders_low):
        checks.append(pattern_check(claim, peak.coef))
    if not found:
        verdict = NOT_REPRODUCED
    elif all(c.passed for c in checks):
        verdict = REPRODUCED
    else:
        verdict = PARTLY
    return Verdict(claim.id, claim.kind, verdict, checks, observed)


def _check_pattern(claim: Claim, results: RunResults) -> Verdict:
    peak, checks, observed = _find_peak(claim, results)
    if peak is None or not all(c.passed for c in checks):
        return Verdict(claim.id, claim.kind, NOT_REPRODUCED, checks, observed,
                       reason="no peak above threshold at the claimed position")
    pc = pattern_check(claim, peak.coef)
    checks.append(pc)
    return Verdict(claim.id, claim.kind, REPRODUCED if pc.passed else NOT_REPRODUCED, checks, observed)


def _check_absent(claim: Claim, results: RunResults) -> Verdict:
    assert claim.trait and claim.chr is not None and claim.pos_mb is not None
    half = position_half_width(claim)
    threshold = claim.tol("threshold_lod")
    lo, hi = claim.pos_mb - half, claim.pos_mb + half
    window = results.profile.window_max(claim.trait, claim.chr, lo, hi)
    if window is None:
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE,
                       reason=f"no markers on chr {claim.chr} between {lo:g} and {hi:g} {claim.units}")
    max_lod, max_pos = window
    check = Check("stays below threshold", max_lod < threshold, f"max LOD < {threshold:g}",
                  f"{max_lod:.2f} at {max_pos:g} {claim.units}", f"window ±{half:g} {claim.units}")
    return Verdict(claim.id, claim.kind, REPRODUCED if check.passed else NOT_REPRODUCED, [check],
                   {"window_mb": [lo, hi], "window_max_lod": max_lod, "window_max_pos": max_pos})


def _check_count(claim: Claim, results: RunResults) -> Verdict:
    assert claim.value is not None
    threshold = claim.tol("threshold_lod")
    missing = [t for t in claim.traits if t not in results.traits]
    if missing:
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE, reason=f"traits not in results: {missing}")
    if results.report_threshold > threshold:
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE,
                       reason=f"engine only reported peaks above LOD {results.report_threshold:g}")
    n = sum(1 for p in results.peaks if p.trait in claim.traits and p.lod >= threshold)
    rel = claim.tol("count_rel")
    ok = abs(n - claim.value) <= rel * claim.value
    check = Check("count", ok, f"{claim.value:g}", f"{n}", f"±{rel:.0%}")
    return Verdict(claim.id, claim.kind, REPRODUCED if ok else NOT_REPRODUCED, [check], {"count": n})


def _check_perm(claim: Claim, results: RunResults) -> Verdict:
    assert claim.value is not None and claim.alpha is not None
    key = f"alpha_{claim.alpha:g}"
    thr = (results.permutation_thresholds or {}).get(claim.trait or "", {}).get(key)
    if thr is None:
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE,
                       reason=f"no permutation threshold at alpha {claim.alpha:g} for {claim.trait} "
                              "(set n_perm and perm_alpha in run.yaml)")
    allow = claim.tol("lod_abs")
    ok = abs(thr - claim.value) <= allow
    check = Check(f"permutation threshold (alpha {claim.alpha:g})", ok, f"{claim.value:g}", f"{thr:.2f}",
                  f"±{allow:g}", f"difference {thr - claim.value:+.2f}")
    return Verdict(claim.id, claim.kind, REPRODUCED if ok else NOT_REPRODUCED, [check], {"threshold": thr})


_DISPATCH = {
    "perm_threshold": _check_perm,
    "qtl_peak": _check_peak,
    "qtl_absent": _check_absent,
    "effect_pattern": _check_pattern,
    "count": _check_count,
}


def compare_claim(claim: Claim, results: RunResults) -> Verdict:
    if claim.trait and claim.trait not in results.traits:
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE,
                       reason=f"trait {claim.trait!r} was not mapped in this run")
    if claim.kind in ("qtl_peak", "effect_pattern") and results.report_threshold > claim.tol("threshold_lod"):
        return Verdict(claim.id, claim.kind, NOT_CHECKABLE,
                       reason=f"engine only reported peaks above LOD {results.report_threshold:g}, "
                              f"above the claim's threshold {claim.tol('threshold_lod'):g}")
    return _DISPATCH[claim.kind](claim, results)


def compare_all(claims: list[Claim], results: RunResults) -> list[Verdict]:
    return [compare_claim(c, results) for c in claims]


def tally(verdicts: list[Verdict]) -> dict[str, int]:
    return {v: sum(1 for x in verdicts if x.verdict == v) for v in VERDICTS}
