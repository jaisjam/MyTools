#!/bin/bash
# vSim: Verilog simulation wrapper

set -e

OUT_FILE="$1"
SRC_FILE="$2"

if [[ -z "$OUT_FILE" || -z "$SRC_FILE" ]]; then
  echo "Usage: $0 <output_sim.out> <verilog_source.v>"
  exit 1
fi

echo "Compiling $SRC_FILE to $OUT_FILE"
iverilog -o "$OUT_FILE" "$SRC_FILE"

echo "Running simulation..."
vvp "$OUT_FILE"

# Optional waveform capture
if [[ -f waveform.vcd ]]; then
  echo "Moving waveform.vcd to ../bin/"
  mv waveform.vcd ../bin/waveform.vcd
fi

echo "Simulation completed !!"
