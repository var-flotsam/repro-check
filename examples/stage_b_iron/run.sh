#!/usr/bin/env bash
# Stage B warm-up end to end. Needs network access to raw.githubusercontent.com
# and Rscript with qtl2 on PATH (see env/).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
name="$(basename "$here")"
run="${1:-$here/../../runs/$name}"
rm -rf "$run"
mkdir -p "$run"
cp "$here/claims.yaml" "$run/claims.frozen.yaml"
: "${REPRO_CHECK_CONFIRMED_BY:?set to the name of the person who confirmed claims.yaml}"
repro-check freeze "$run/claims.frozen.yaml" --by "$REPRO_CHECK_CONFIRMED_BY"
repro-check fetch "$here/inputs.yaml" --run "$run"
repro-check run "$here/run.yaml" --run "$run"
repro-check compare "$run/claims.frozen.yaml" --run "$run"
repro-check report "$run/claims.frozen.yaml" --run "$run"
