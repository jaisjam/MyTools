#!/bin/bash
# This script must be sourced to properly activate the OSS CAD Suite environment.

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "ERROR!: You must run this using: source fpga-env"
    echo "    (Do NOT run it directly)"
    exit 1
fi

# Source the OSS CAD Suite environment
source /repo/ejamjai/Compiler/oss-cad-suite/environment

echo "OSS CAD Suite environment is now active."

