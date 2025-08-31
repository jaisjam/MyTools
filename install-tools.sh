#!/bin/bash
# Installer: setup FPGA helper tools, install dependencies, and create symlinks in /usr/bin

set -e

TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Installing FPGA helper tools from $TOOLS_DIR"
echo

# --------------------------
# 1. Install system packages
# --------------------------
echo "[1/4] Installing system dependencies..."
sudo apt update
sudo apt install -y build-essential cmake git \
                    iverilog gtkwave libftdi1-2 libusb-1.0-0
echo "System dependencies installed."
echo

# --------------------------
# 2. Lock down permissions
# --------------------------
echo "[2/4] Setting script permissions (read+execute only)..."
chmod 555 "$TOOLS_DIR/icegen"
chmod 555 "$TOOLS_DIR/vSimBuild.sh"
chmod 555 "$TOOLS_DIR/gtk_wave.sh"
chmod 555 "$TOOLS_DIR/fpga_env.sh"
echo "Permissions set."
echo

# --------------------------
# 3. Create symlinks
# --------------------------
echo "[3/4] Creating symlinks in /usr/bin..."
sudo ln -sf "$TOOLS_DIR/icegen"        /usr/bin/icegen
sudo ln -sf "$TOOLS_DIR/vSimBuild.sh"  /usr/bin/vSim
sudo ln -sf "$TOOLS_DIR/gtk_wave.sh"   /usr/bin/gtkwave-safe
sudo ln -sf "$TOOLS_DIR/fpga_env.sh"   /usr/bin/fpga-env
echo "Symlinks created."
echo

# --------------------------
# 4. Check OSS CAD Suite tools
# --------------------------
echo "[4/4] Checking OSS CAD Suite tools..."
MISSING=()

for TOOL in yosys nextpnr-ice40 icepack iceprog; do
    if ! command -v "$TOOL" >/dev/null 2>&1; then
        MISSING+=("$TOOL")
    fi
done

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ All required OSS CAD Suite tools are available."
else
    echo "⚠️  Warning: The following tools are missing: ${MISSING[*]}"
    echo "    Make sure OSS CAD Suite is installed and 'source fpga-env' is run before building."
fi
echo

echo "✅ Installation complete!"
echo
echo "Now you can use:"
echo "  icegen         → project generator"
echo "  vSim           → Verilog simulation wrapper"
echo "  gtkwave-safe   → safe GTKWave launcher"
echo "  source fpga-env → activate OSS CAD Suite environment"

