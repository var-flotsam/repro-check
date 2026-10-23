"""Write the Markdown report from frozen claims, verdicts and provenance.

The report only restates what compare.py decided. Wording is neutral: a
claim is reproduced or not within the stated tolerance, with the numbers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .claims import ClaimsFile
from .compare import VERDICTS, Verdict, tally
from .founders import label


def _short(claim) -> str:
    if claim.kind == "perm_threshold":
        return f"{claim.trait}: LOD threshold {claim.value:g} at alpha {claim.alpha:g}"
    if claim.kind == "count":
        return f"{claim.value:g} QTL above LOD {claim.tol('threshold_lod'):g}"
    where = f"chr {claim.chr} ~{claim.pos_mb:g} {claim.units}"
    if claim.kind == "qtl_absent":
        return f"{claim.trait}: no QTL at {where}"
    bits = [f"{claim.trait}: QTL at {where}"]
    if claim.lod is not None:
        bits.append(f"LOD {claim.lod:g}")
    if claim.founders_high:
        bits.append(f"{label(claim.founders_high)} high")
    if claim.founders_low:
        bits.append(f"{label(claim.founders_low)} low")
    return ", ".join(bits)


def _observed(v: Verdict, units: str) -> str:
    o = v.observed
    if v.verdict == "not checkable":
        return v.reason
    if "threshold" in o:
        return f"{o['threshold']:.2f}"
    if "count" in o:
        return f"{o['count']}"
    if "lod" in o:
        return f"chr {o['chr']} {o['pos']:g} {units}, LOD {o['lod']:.2f}"
    if "window_max_lod" in o:
        return f"max LOD {o['window_max_lod']:.2f} at {o['window_max_pos']:g} {units}"
    return v.reason or "—"


def _cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render(claims: ClaimsFile, verdicts: list[Verdict], run_dir: Path) -> str:
    by_id = claims.by_id()
    prov = _read_json(run_dir / "provenance.json") or {"inputs": {}}
    env = _read_json(run_dir / "environment.json") or {}
    results = _read_json(run_dir / "engine" / "results.json") or {}
    run_cfg = _read_yaml(run_dir / "run_config.yaml") or {}
    counts = tally(verdicts)
    paper = claims.paper
    frozen = claims.frozen or {}

    out: list[str] = []
    out.append(f"# Reproduction report: {paper.get('citation') or paper['doi']}")
    out.append("")
    out.append(f"- DOI: {paper['doi']}")
    out.append(f"- Run: `{run_dir.name}`")
    out.append(f"- Claims frozen by {frozen.get('by', '—')} at {frozen.get('at', '—')}, "
               f"sha256 `{frozen.get('sha256', '—')}`")
    out.append("- Result: " + ", ".join(f"{counts[k]} {k}" for k in VERDICTS if counts[k]))
    out.append("")
    out.append("Verdicts are computed by `repro_check.compare` against tolerances fixed before "
               "the run. \"Not reproduced\" means the number fell outside the stated tolerance "
               "in this rerun; it says nothing about why.")
    out.append("")

    out.append("## Results")
    out.append("")
    out.append("| Claim | What the paper reports | Observed | Verdict |")
    out.append("|---|---|---|---|")
    for v in verdicts:
        c = by_id[v.claim_id]
        out.append(f"| {c.id} | {_cell(_short(c))} | {_cell(_observed(v, c.units))} | **{v.verdict}** |")
    out.append("")

    out.append("## Claim details")
    out.append("")
    for v in verdicts:
        c = by_id[v.claim_id]
        out.append(f"### {c.id}: {v.verdict}")
        out.append("")
        out.append(f"- Source: {c.source}")
        out.append(f"- Quote: \"{c.quote}\"")
        if c.trait:
            n = (results.get("n_mapped") or {}).get(c.trait)
            out.append(f"- Trait: `{c.trait}`" + (f" (N = {n})" if n is not None else ""))
        if v.reason:
            out.append(f"- Note: {v.reason}")
        if v.checks:
            out.append("")
            out.append("| Check | Claimed | Observed | Tolerance | Pass |")
            out.append("|---|---|---|---|---|")
            for ch in v.checks:
                obs = ch.observed + (f" ({ch.detail})" if ch.detail else "")
                out.append(f"| {ch.name} | {_cell(ch.claimed)} | {_cell(obs)} | {_cell(ch.tolerance)} | "
                           f"{'yes' if ch.passed else 'no'} |")
        if c.notes:
            out.append("")
            out.append(f"Notes: {c.notes}")
        out.append("")

    out.append("## Assumptions")
    out.append("")
    assumptions = list(run_cfg.get("assumptions") or [])
    model = [
        f"Covariates: {', '.join(run_cfg.get('addcovar') or []) or 'none'}"
        + (f" (as factors: {', '.join(run_cfg['covar_factors'])})" if run_cfg.get("covar_factors") else ""),
        f"Kinship: {run_cfg.get('kinship', 'loco')}",
        f"Allele effects: {'scan1blup' if run_cfg.get('effects', 'blup') == 'blup' else 'scan1coef'}",
        f"Support interval: {run_cfg.get('ci_drop', 1.5)}-LOD drop",
    ]
    for i, a in enumerate(assumptions + model, 1):
        out.append(f"{i}. {a}")
    for trait, note in (results.get("notes") or {}).items():
        out.append(f"- `{trait}`: {note}")
    out.append("")

    out.append("## Inputs")
    out.append("")
    out.append("| Input | Source | Retrieved | Bytes | sha256 |")
    out.append("|---|---|---|---|---|")
    for name, rec in (prov.get("inputs") or {}).items():
        out.append(f"| {name} | {_cell(rec['url'])} | {rec['retrieved_at']} | {rec['bytes']} | "
                   f"`{rec['sha256']}` |")
    out.append("")

    out.append("## Environment")
    out.append("")
    eng = results.get("engine") or {}
    out.append(f"- Engine: {eng.get('name', '—')}, {eng.get('r_version', '—')}, "
               f"qtl2 {eng.get('qtl2_version', '—')}")
    out.append(f"- repro-check {env.get('repro_check', '—')}, Python {env.get('python', '—')}")
    out.append(f"- Seed: {run_cfg.get('seed', '—')}; permutations: {run_cfg.get('n_perm', 0)}")
    out.append(f"- Samples: {results.get('n_samples', '—')}; markers: {results.get('n_markers', '—')}")
    out.append("- Full R session info: `engine/session_info.txt`")
    out.append("")

    out.append("## Ambiguities")
    out.append("")
    amb = run_cfg.get("ambiguities") or []
    out.extend(f"- {a}" for a in amb) if amb else out.append("None recorded.")
    out.append("")
    return "\n".join(out)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text()) if path.exists() else None


def _read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text()) if path.exists() else None
