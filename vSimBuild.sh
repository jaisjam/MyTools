#!/bin/bash
# vSim: Verilog simulation wrapper

set -e

OUT_FILE="$1"
shift
SRC_FILES=("$@")

if [[ -z "$OUT_FILE" || ${#SRC_FILES[@]} -eq 0 ]]; then
  echo "Usage: $0 <output_sim.out> <verilog_source.v ...>"
  exit 1
fi

# Collect unique include directories from all sources
INCLUDE_DIRS=()
for f in "${SRC_FILES[@]}"; do
  dir=$(dirname "$f")
  if [[ ! " ${INCLUDE_DIRS[*]} " =~ " $dir " ]]; then
    INCLUDE_DIRS+=("-I$dir")
  fi
done

echo "Compiling ${SRC_FILES[*]} to $OUT_FILE"
iverilog "${INCLUDE_DIRS[@]}" -o "$OUT_FILE" "${SRC_FILES[@]}"

echo "Running simulation..."
vvp "$OUT_FILE"

echo "Simulation completed !!"

