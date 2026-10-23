#!/usr/bin/env bash
# Stage A end to end. Needs Rscript with qtl2 on PATH (see env/).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
run="${1:-$here/../../runs/stage_a}"
rm -rf "$run" "$here/sim"
mkdir -p "$run"
cp "$here/claims.yaml" "$run/claims.frozen.yaml"
repro-check simulate "$here/spec.json" "$here/sim"
repro-check freeze "$run/claims.frozen.yaml" --by "stage-a (synthetic, known answers)"
repro-check fetch "$here/inputs.yaml" --run "$run"
repro-check run "$here/run.yaml" --run "$run"
repro-check compare "$run/claims.frozen.yaml" --run "$run"
repro-check report "$run/claims.frozen.yaml" --run "$run"
