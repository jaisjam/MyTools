#!/usr/bin/env python3
import os
from AIRXX_aireWetICEgenBase import IceGen

class IceGenHw(IceGen):
    def create_hw_structure(self, base, device, top, template):
        gw_base = os.path.join(base, "gateware")
        os.makedirs(gw_base, exist_ok=True)
        os.makedirs(os.path.join(gw_base, "build"), exist_ok=True)
        self._write_hw_cmakelists(gw_base, device, top)
        self._write_sample_verilog(gw_base, top, template)
        self._write_sample_pcf(gw_base, top, device)
        self._write_vscode_config(gw_base, top)

    def _write_hw_cmakelists(self, gw_base, device, top):
        path = os.path.join(gw_base, "CMakeLists.txt")
        log_path = "AireWetIceBreaker++.log"
        with open(path, "w") as f:
            f.write("cmake_minimum_required(VERSION 3.12)\n")
            f.write(f"project({top}_ice40)\n\n")
            f.write("set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})\n")
            f.write(f"set(TOP {top})  # Change this to your actual top-level module name\n")
            f.write(f"set(BUILD_LOG {log_path})\n\n")
            f.write("set(PIN_CONSTRAINTS ${CMAKE_CURRENT_SOURCE_DIR}/${TOP}.pcf)\n")
            f.write("set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${PIN_CONSTRAINTS})\n\n")

            f.write('file(GLOB_RECURSE VERILOG_SOURCES "${CMAKE_SOURCE_DIR}/gateware/*.v" "${CMAKE_SOURCE_DIR}/gateware/*.vh")\n\n')

            f.write("add_custom_target(sim\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"[25%] Simulation...\"\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E make_directory ../bin\n")
            f.write("    COMMAND bash -c 'vSim ../bin/sim.out ${VERILOG_SOURCES} >> \"${BUILD_LOG}\" 2>&1'\n")
            f.write("    COMMENT \"Simulation step\"\n")
            f.write(")\n\n")

            f.write("add_custom_target(synth\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"[50%] Synthesizing...\"\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"read_verilog ${VERILOG_SOURCES}\" > ${CMAKE_BINARY_DIR}/synth.ys\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"hierarchy -check -top ${TOP}\" >> ${CMAKE_BINARY_DIR}/synth.ys\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"synth_ice40 -top ${TOP} -json ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${TOP}.json\" >> ${CMAKE_BINARY_DIR}/synth.ys\n")
            f.write("    COMMAND yosys -s ${CMAKE_BINARY_DIR}/synth.ys >> \"${BUILD_LOG}\" 2>&1\n")
            f.write("    DEPENDS sim\n")
            f.write("    COMMENT \"Synthesizing step\"\n")
            f.write(")\n\n")

            f.write("add_custom_target(pnr\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"[75%] Placing and Routing...\"\n")
            f.write(
                "    COMMAND bash -c 'nextpnr-ice40 --%s --package sg48 --json ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${TOP}.json --pcf ${PIN_CONSTRAINTS} --asc ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${TOP}.asc >> \"${BUILD_LOG}\" 2>&1'\n"
                % device
            )
            f.write("    DEPENDS synth ${PIN_CONSTRAINTS}\n")
            f.write("    COMMENT \"Placing and Routing step\"\n")
            f.write(")\n\n")

            f.write("add_custom_target(bitstream\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"[100%] Bitstream...\"\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E make_directory ../bin\n")
            f.write("    COMMAND bash -c 'icepack ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${TOP}.asc ../bin/${TOP}.bin >> \"${BUILD_LOG}\" 2>&1'\n")
            f.write("    DEPENDS pnr\n")
            f.write("    COMMENT \"Bitstream step\"\n")
            f.write(")\n\n")

            f.write("add_custom_target(fpga\n")
            f.write("    DEPENDS bitstream\n")
            f.write("    COMMENT \"FPGA binary build (simulation + synth + pnr + bitstream)\"\n")
            f.write(")\n\n")

            f.write("add_custom_target(flash\n")
            f.write("    COMMAND ${CMAKE_COMMAND} -E echo \"[100%] Flashing to FPGA\"\n")
            f.write("    COMMAND bash -c 'iceprog ../bin/${TOP}.bin >> \"${BUILD_LOG}\" 2>&1'\n")
            f.write("    COMMENT \"Flash .bin to FPGA\"\n")
            f.write(")\n")

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
