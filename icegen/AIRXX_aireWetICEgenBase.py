#!/usr/bin/env python3
import argparse
import sys
import os
from argparse import RawTextHelpFormatter

class IceGen:
    __VERSION = "0.018"

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description="🧊 icegen: iCE40 CMake project generator",
            usage="icegen [-p] [-t [name]] [-d device] [-v]",
            formatter_class=RawTextHelpFormatter
        )
        self._setup_arguments()

    def _setup_arguments(self):
        self._parser.add_argument("-p", "--project", dest="project", metavar="", help="Create a new iCE40 project")
        self._parser.add_argument("-t", "--template", dest="template", nargs="?", const="sample", default="none", metavar="", help="Template name")
        self._parser.add_argument("-d", "--device", dest="device", default="up5k", metavar="", help="Target device")
        self._parser.add_argument("-v", "--version", action="store_true", help="Show version and exit")

    def parse_args(self):
        args = self._parser.parse_args()
        if args.version:
            print(f"icegen version {self.__VERSION}")
            sys.exit(0)
        if not args.project:
            self._parser.print_help()
            sys.exit(1)
        return args

    def write_root_cmakelists(self, base_dir, project_name):
        path = os.path.join(base_dir, "CMakeLists.txt")
        with open(path, "w") as f:
            f.write("cmake_minimum_required(VERSION 3.16)\n")
            f.write(f"project({project_name}_full)\n\n")
            f.write("enable_language(C)\n")
            f.write("enable_language(CXX)\n\n")
            f.write("if(EXISTS ${CMAKE_SOURCE_DIR}/gateware)\n    add_subdirectory(gateware)\nendif()\n\n")
            f.write("if(EXISTS ${CMAKE_SOURCE_DIR}/software)\n    add_subdirectory(software)\nendif()\n\n")
            f.write("add_custom_target(fpga_platform_all COMMENT \"Build FPGA app + FPGA bitstream\")\n")
            f.write("if(TARGET fpga)\n    add_dependencies(fpga_platform_all fpga)\nendif()\n")
            f.write("if(TARGET runTests)\n    add_dependencies(fpga_platform_all runTests)\nendif()\n")

    def write_root_readme(self, base_dir, project_name):
        path = os.path.join(base_dir, "README.md")
        with open(path, "w") as f:
            f.write(f"# {project_name} FPGA Platform Project\n\n")
            f.write("## 🛠 Combined Build (Recommended)\n\n")
            f.write("```sh\nmkdir -p build && cd build\ncmake ..\ncmake --build . --target fpga_platform_all -j4\n```\n\n")
            f.write("The `fpga_platform_all` target builds the FPGA bitstream and the software payload in one step.\n\n")
            f.write("## ⚙️ Module Build (Advanced)\n\n")
            f.write("### FPGA\n```sh\ncd build\ncmake ..\ncmake --build . --target fpga -j4\ncmake --build . --target flash\n```\n")
            f.write("### Software\n```sh\ncd build\ncmake ..\ncmake --build . --target fpga_platform -j4\ncmake --build . --target runTests\nctest --output-on-failure\n```\n")
