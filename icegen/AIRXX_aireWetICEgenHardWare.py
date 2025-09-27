#!/usr/bin/env python3
import os
from AIRXX_aireWetICEgenBase import IceGen

class IceGenHw(IceGen):
    def create_hw_structure(self, base, device, top, template):
        gw_base = os.path.join(base, "gateware")
        os.makedirs(gw_base, exist_ok=True)
        self._write_hw_cmakelists(gw_base, device, top)
        self._write_sample_verilog(gw_base, top, template)
        self._write_sample_pcf(gw_base, top, device)
        self._write_vscode_config(gw_base, top)

    def _write_hw_cmakelists(self, gw_base, device, top):
        path = os.path.join(gw_base, "CMakeLists.txt")
        with open(path, "w") as f:
            f.write("cmake_minimum_required(VERSION 3.12)\n")
            f.write(f"project({top}_ice40)\n\n")
            f.write("set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})\n")
            f.write(f"set(TOP {top})\nset(BUILD_LOG AireWetIceBreaker++.log)\n\n")
            f.write('file(GLOB_RECURSE VERILOG_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/*.v" "${CMAKE_CURRENT_SOURCE_DIR}/*.vh")\n')
            f.write('string(REPLACE ";" " " VERILOG_SOURCES_FLAT "${VERILOG_SOURCES}")\n')
            f.write('if(VERILOG_SOURCES)\n')
            f.write('    set(YOSYS_READ_CMD "read_verilog ${VERILOG_SOURCES_FLAT}; ")\n')
            f.write('else()\n')
            f.write('    set(YOSYS_READ_CMD "")\n')
            f.write('endif()\n\n')
            f.write("add_custom_target(sim COMMAND echo Sim COMMENT \"Simulation\")\n")
            f.write("add_custom_target(synth COMMAND yosys -p \"${YOSYS_READ_CMD}synth_ice40 -top ${TOP} -json ${TOP}.json\" DEPENDS sim)\n")
            f.write(f"add_custom_target(pnr COMMAND nextpnr-ice40 --{device} --json ${{TOP}}.json --pcf ${{TOP}}.pcf --asc ${{TOP}}.asc DEPENDS synth)\n")
            f.write("add_custom_target(bitstream COMMAND icepack ${TOP}.asc ${TOP}.bin DEPENDS pnr)\n")
            f.write("add_custom_target(fpga DEPENDS bitstream)\n")
            f.write("add_custom_target(flash COMMAND iceprog ${TOP}.bin DEPENDS bitstream)\n")

    def _write_sample_verilog(self, gw_base, top, template):
        if template == "none": return
        with open(os.path.join(gw_base, f"{top}.v"), "w") as f:
            f.write(f"module {top}(input clk, output reg led); always @(posedge clk) led<=~led; endmodule\n")

    def _write_sample_pcf(self, gw_base, top, device):
        with open(os.path.join(gw_base, f"{top}.pcf"), "w") as f:
            f.write(f"# PCF for {top} on {device}\n# TODO: add pins\n")

    def _write_vscode_config(self, gw_base, top):
        vs = os.path.join(gw_base, ".vscode")
        os.makedirs(vs, exist_ok=True)
        with open(os.path.join(vs, "settings.json"), "w") as f:
            f.write("{\"files.associations\":{\"*.v\":\"verilog\",\"*.pcf\":\"plaintext\"}}")
