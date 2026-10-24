"""Command line: repro-check {validate,freeze,fetch,run,compare,figures,report,simulate}.

Typical run, each step reading the previous step's files in RUN/:

    repro-check validate claims.yaml
    repro-check freeze claims.yaml --by "Name"      # after the user confirms
    repro-check fetch inputs.yaml --run RUN
    repro-check run run.yaml --run RUN --claims claims.yaml
    repro-check compare claims.yaml --run RUN
    repro-check figures claims.yaml --run RUN      # if the claims declare figures
    repro-check report claims.yaml --run RUN
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import claims as claims_mod
from . import compare as compare_mod
from . import fetch as fetch_mod
from . import report as report_mod
from . import results as results_mod
from . import run as run_mod


def _validate(a) -> int:
    cf = claims_mod.load(a.claims)
    state = "frozen" if cf.frozen else "not frozen"
    print(f"{a.claims}: {len(cf.claims)} claims, valid, {state}")
    return 0


def _freeze(a) -> int:
    digest = claims_mod.freeze(a.claims, a.by)
    print(f"frozen: sha256 {digest}")
    return 0


def _fetch(a) -> int:
    prov = fetch_mod.fetch(a.manifest, a.run)
    for name, rec in prov["inputs"].items():
        print(f"{name}: {rec['bytes']} bytes, sha256 {rec['sha256']}")
    return 0


def _figures_of(a) -> list:
    """Figures from a separate frozen figures file if given, else from the claims file."""
    if getattr(a, "figures", None):
        return claims_mod.load_frozen(a.figures).figures
    return claims_mod.load_frozen(a.claims).figures if a.claims else []


def _run(a) -> int:
    figures = _figures_of(a)
    out = run_mod.run(a.config, a.run, figures)
    print(f"engine output in {out}")
    return 0


def _compare(a) -> int:
    cf = claims_mod.load_frozen(a.claims)
    run_dir = Path(a.run)
    shutil.copyfile(a.claims, run_dir / "claims.yaml")
    res = results_mod.load(run_dir / "engine")
    verdicts = compare_mod.compare_all(cf.claims, res)
    payload = {"claims_sha256": cf.frozen["sha256"], "verdicts": [v.to_dict() for v in verdicts],
               "tally": compare_mod.tally(verdicts)}
    (run_dir / "verdicts.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    for v in verdicts:
        print(f"{v.claim_id}: {v.verdict}")
    return 0


def _figures(a) -> int:
    cf = claims_mod.load_frozen(a.claims)
    figures = _figures_of(a)
    if not figures:
        print("no figures declared")
        return 0
    units = cf.paper.get("position_units", "Mb")
    out = run_mod.draw_figures(figures, a.run, units, claims_mod.DEFAULT_TOLERANCE["threshold_lod"])
    print(f"figures in {out}")
    return 0


def _report(a) -> int:
    cf = claims_mod.load_frozen(a.claims)
    run_dir = Path(a.run)
    payload = json.loads((run_dir / "verdicts.json").read_text(encoding="utf-8"))
    if payload["claims_sha256"] != cf.frozen["sha256"]:
        raise claims_mod.ClaimsError("verdicts.json was computed from different claims; rerun compare")
    verdicts = [
        compare_mod.Verdict(**{**v, "checks": [compare_mod.Check(**c) for c in v["checks"]]})
        for v in payload["verdicts"]
    ]
    figfile = claims_mod.load_frozen(a.figures) if a.figures else None
    text = report_mod.render(cf, verdicts, run_dir, figfile)
    out = Path(a.out) if a.out else run_dir / "report.md"
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def _simulate(a) -> int:
    out = run_mod.simulate(a.spec, a.out_dir)
    print(f"simulated data in {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="repro-check", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate", help="check a claims file")
    p.add_argument("claims")
    p.set_defaults(func=_validate)
    p = sub.add_parser("freeze", help="record confirmation and hash of the claims")
    p.add_argument("claims")
    p.add_argument("--by", required=True, help="who confirmed the claims")
    p.set_defaults(func=_freeze)
    p = sub.add_parser("fetch", help="download inputs and record checksums")
    p.add_argument("manifest")
    p.add_argument("--run", required=True)
    p.set_defaults(func=_fetch)
    p = sub.add_parser("run", help="run the engine")
    p.add_argument("config")
    p.add_argument("--run", required=True)
    p.add_argument("--claims", help="frozen claims file; its allele_effects figures add effect regions")
    p.add_argument("--figures", help="separate frozen figures file (overrides figures in --claims)")
    p.set_defaults(func=_run)
    p = sub.add_parser("compare", help="compute verdicts")
    p.add_argument("claims")
    p.add_argument("--run", required=True)
    p.set_defaults(func=_compare)
    p = sub.add_parser("figures", help="redraw the declared paper figures (no verdicts)")
    p.add_argument("claims")
    p.add_argument("--run", required=True)
    p.add_argument("--figures", help="separate frozen figures file")
    p.set_defaults(func=_figures)
    p = sub.add_parser("report", help="write the Markdown report")
    p.add_argument("claims")
    p.add_argument("--run", required=True)
    p.add_argument("--out")
    p.add_argument("--figures", help="separate frozen figures file")
    p.set_defaults(func=_report)
    p = sub.add_parser("simulate", help="make synthetic data with planted QTL")
    p.add_argument("spec")
    p.add_argument("out_dir")
    p.set_defaults(func=_simulate)
    a = ap.parse_args(argv)
    try:
        return a.func(a)
    except (claims_mod.ClaimsError, fetch_mod.FetchError, run_mod.RunError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
