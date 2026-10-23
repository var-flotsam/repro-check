"""Create (or lock) the pinned R environment with py-rattler.

    uv run --group renv python scripts/make_r_env.py PREFIX          # install
    uv run --group renv python scripts/make_r_env.py --lock          # rewrite env/r-linux-64.lock

The specs come from env/r-environment.yml. The lock file is a conda
"explicit" spec (URL#md5), installable with
`micromamba create -p PREFIX -f env/r-linux-64.lock`.
"""

import argparse
import asyncio
import pathlib

import yaml
from rattler import Platform, VirtualPackage, install, solve

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / "env" / "r-environment.yml"
LOCK_FILE = ROOT / "env" / "r-linux-64.lock"


async def _solve():
    env = yaml.safe_load(ENV_FILE.read_text())
    return await solve(
        sources=env["channels"],
        specs=env["dependencies"],
        platforms=[Platform.current(), Platform("noarch")],
        virtual_packages=VirtualPackage.detect(),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?")
    ap.add_argument("--lock", action="store_true")
    args = ap.parse_args()
    records = asyncio.run(_solve())
    if args.lock:
        lines = ["@EXPLICIT"] + sorted(f"{r.url}#{r.md5.hex()}" for r in records)
        LOCK_FILE.write_text("\n".join(lines) + "\n")
        print(f"wrote {LOCK_FILE} ({len(records)} packages)")
    if args.prefix:
        asyncio.run(install(records, target_prefix=args.prefix))
        print(f"installed {len(records)} packages into {args.prefix}")
    if not (args.lock or args.prefix):
        ap.error("give PREFIX and/or --lock")


if __name__ == "__main__":
    main()
