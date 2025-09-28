#!/usr/bin/env python3
import os
from AIRXX_aireWetICEgenBase import IceGen

class IceGenSw(IceGen):
    def create_sw_structure(self, base):
        sw_base = os.path.join(base, "software")
        os.makedirs(sw_base, exist_ok=True)
        os.makedirs(os.path.join(sw_base, "build"), exist_ok=True)
        for sub in ["icemodule/src","icemodule/inc","icelib","test/src","test/inc"]:
            os.makedirs(os.path.join(sw_base, sub), exist_ok=True)
        main_cpp = os.path.join(sw_base, "main.cpp")
        if not os.path.exists(main_cpp):
            with open(main_cpp,"w") as f:
                f.write('#include <iostream>\n#include "logger.h"\nint main(){std::cout<<"Hello from FPGA platform app!"<<std::endl; log_message("test");return 0;}')
        self._create_airelib(sw_base)
        self._write_sw_cmakelists(sw_base)

    def _create_airelib(self, sw_base):
        with open(os.path.join(sw_base,"icelib/icelib.h"),"w") as f:
            f.write("#pragma once\n#include <stdio.h>\n#include <string.h>\n#include <iostream>")

    def _write_sw_cmakelists(self, project_root: str):
        cmake_path = os.path.join(project_root, "CMakeLists.txt")
        with open(cmake_path, "w") as f:
            # Minimum required CMake version & project
            f.write("# Minimum required CMake version & project\n")
            f.write("cmake_minimum_required(VERSION 3.16)\n\n")
            f.write("project(AireWetHwUart LANGUAGES CXX)\n\n")

            # C++ standard configuration
            f.write("# C++ standard configuration\n")
            f.write("set(CMAKE_CXX_STANDARD 17)\n")
            f.write("set(CMAKE_CXX_STANDARD_REQUIRED ON)\n")
            f.write("set(CMAKE_CXX_EXTENSIONS OFF)\n\n")

            # Build options
            f.write("# Build options\n")
            f.write("option(BUILD_TESTS \"Build unit tests with GoogleTest\" OFF)\n")
            f.write("option(BUILD_SIMULATION \"Build simulation (main executable)\" OFF)\n")
            f.write("option(BUILD_PRODUCT \"Build shared product library (.so/.dll)\" OFF)\n\n")

            # Default mode selection
            f.write("# Default to product mode if no flag is set\n")
            f.write("if(NOT BUILD_TESTS AND NOT BUILD_SIMULATION AND NOT BUILD_PRODUCT)\n")
            f.write("    set(BUILD_PRODUCT ON)\n")
            f.write("endif()\n\n")

            # Output directories
            f.write("# Output directories\n")
            f.write("set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n")
            f.write("set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n")
            f.write("set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n\n")

            # Collect sources
            f.write("# Collect sources\n")
            f.write("file(GLOB ICE_MODULE_SRC ${CMAKE_CURRENT_SOURCE_DIR}/icemodule/src/*.cpp)\n")
            f.write("file(GLOB ICE_MAIN_SRC ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)\n")
            f.write("file(GLOB ICE_TEST_SRC ${CMAKE_CURRENT_SOURCE_DIR}/test/src/*.cpp)\n\n")

            # Core iCE library
            f.write("# Core iCE library\n")
            f.write("add_library(iCEmodule STATIC ${ICE_MODULE_SRC})\n")
            f.write("target_include_directories(iCEmodule PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/icemodule/inc)\n\n")

            # Header-only wrapper
            f.write("# Header-only wrapper\n")
            f.write("add_library(iCE_libery INTERFACE)\n")
            f.write("target_include_directories(iCE_libery INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/icelib)\n\n")

            # Simulation mode
            f.write("# Simulation mode\n")
            f.write("if(BUILD_SIMULATION)\n")
            f.write("    add_executable(iCEsimulation ${ICE_MAIN_SRC})\n")
            f.write("    target_link_libraries(iCEsimulation PRIVATE iCEmodule iCE_libery)\n")
            f.write("    target_include_directories(iCEsimulation PRIVATE\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/icemodule/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/icelib\n")
            f.write("    )\n")
            f.write("endif()\n\n")

            # Product mode
            f.write("# Product mode\n")
            f.write("if(BUILD_PRODUCT)\n")
            f.write("    add_library(iCEshared SHARED ${ICE_MODULE_SRC})\n")
            f.write("    target_include_directories(iCEshared PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/icemodule/inc)\n")
            f.write("    set_target_properties(iCEshared PROPERTIES\n")
            f.write("        CXX_VISIBILITY_PRESET hidden\n")
            f.write("        VISIBILITY_INLINES_HIDDEN YES\n")
            f.write("    )\n")
            f.write("endif()\n\n")

            # Unit test mode
            f.write("# Unit test mode\n")
            f.write("if(BUILD_TESTS)\n")
            f.write("    find_package(GTest REQUIRED)\n")
            f.write("    enable_testing()\n\n")
            f.write("    add_executable(iCEtest ${ICE_TEST_SRC})\n")
            f.write("    target_include_directories(iCEtest PRIVATE\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/test/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/icemodule/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/icelib\n")
            f.write("    )\n")
            f.write("    target_link_libraries(iCEtest PRIVATE\n")
            f.write("        iCEmodule\n")
            f.write("        iCE_libery\n")
            f.write("        GTest::gtest\n")
            f.write("        GTest::gtest_main\n")
            f.write("    )\n\n")
            f.write("    include(GoogleTest)\n")
            f.write("    gtest_discover_tests(iCEtest)\n")
            f.write("endif()\n\n")

            # End of file marker
            f.write("# End of CMakeLists.txt\n")

        print(f"CMakeLists.txt written to {cmake_path}")

