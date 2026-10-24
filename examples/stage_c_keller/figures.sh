#!/usr/bin/env bash
# Redraw the declared Keller figures. Reruns the engine into a separate run
# directory (reusing the fetched inputs) so founder effects along Chr 1 are
# computed, recomputes the verdicts (they should match the first run), then
# draws the figures and writes a report with a Figures section.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="${1:-$here/../../runs/stage_c_keller}"
run="${2:-$here/../../runs/stage_c_keller_figures}"
mkdir -p "$run"
cp "$here/claims.frozen.yaml" "$run/claims.frozen.yaml"
cp "$here/figures.frozen.yaml" "$run/figures.frozen.yaml"
cp -r "$src/inputs" "$src/provenance.json" "$run/"
Rscript "$here/prepare.R" "$run" "$here/trait_map.csv"
repro-check run "$here/run.yaml" --run "$run" --claims "$run/claims.frozen.yaml" --figures "$run/figures.frozen.yaml"
repro-check compare "$run/claims.frozen.yaml" --run "$run"
repro-check figures "$run/claims.frozen.yaml" --run "$run" --figures "$run/figures.frozen.yaml"
repro-check report "$run/claims.frozen.yaml" --run "$run" --figures "$run/figures.frozen.yaml"
