#!/usr/bin/env bash
# Stage C end to end: Keller et al. 2019. Needs network access to
# thejacksonlaboratory.box.com, phenome.jax.org and raw.githubusercontent.com,
# Rscript with qtl2 on PATH (see env/), about 8 GB of RAM and a few GB of disk.
# The claims were frozen before any data was fetched; this script refuses to
# run if they changed.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
run="${1:-$here/../../runs/stage_c_keller}"
mkdir -p "$run"
cp "$here/claims.frozen.yaml" "$run/claims.frozen.yaml"
repro-check validate "$run/claims.frozen.yaml"
[ -f "$run/provenance.json" ] || repro-check fetch "$here/inputs.yaml" --run "$run"
Rscript "$here/prepare.R" "$run" "$here/trait_map.csv"
repro-check run "$here/run.yaml" --run "$run"
repro-check compare "$run/claims.frozen.yaml" --run "$run"
repro-check report "$run/claims.frozen.yaml" --run "$run"
