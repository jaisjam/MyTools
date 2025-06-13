#!/bin/bash

# Safely disable OSS CAD Suite's LD_LIBRARY_PATH to avoid GLIBC errors
unset LD_LIBRARY_PATH

# Path to system GTKWave binary
GTKWAVE_BIN="/usr/bin/gtkwave"

# Verify that GTKWave exists
if [ ! -x "$GTKWAVE_BIN" ]; then
    echo "Error: GTKWave not found at $GTKWAVE_BIN"
    exit 1
fi

# Check for --version or --help anywhere in the args
for arg in "$@"; do
    case "$arg" in
        -v|--version)
            exec "$GTKWAVE_BIN" --version
            ;;
        -h|--help)
            exec "$GTKWAVE_BIN" --help
            ;;
    esac
done

# Launch GTKWave with given arguments or standalone
if [ $# -gt 0 ]; then
    exec "$GTKWAVE_BIN" "$@"
else
    exec "$GTKWAVE_BIN"
fi

