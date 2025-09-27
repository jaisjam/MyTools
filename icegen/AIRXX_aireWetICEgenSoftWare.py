#!/usr/bin/env python3
import os
from AIRXX_aireWetICEgenBase import IceGen

class IceGenSw(IceGen):
    def create_sw_structure(self, base):
        sw_base = os.path.join(base, "software")
        os.makedirs(sw_base, exist_ok=True)
        os.makedirs(os.path.join(sw_base, "build"), exist_ok=True)
        for sub in ["module/src","module/inc","airelib/src","airelib/inc","test/src","test/inc"]:
            os.makedirs(os.path.join(sw_base, sub), exist_ok=True)
        main_cpp = os.path.join(sw_base, "main.cpp")
        if not os.path.exists(main_cpp):
            with open(main_cpp,"w") as f:
                f.write('#include <iostream>\n#include "logger.h"\nint main(){std::cout<<"Hello from FPGA platform app!"<<std::endl; log_message("test");return 0;}')
        self._create_airelib(sw_base)
        self._create_test_example(sw_base)
        self._write_sw_cmakelists(sw_base)

    def _create_airelib(self, sw_base):
        with open(os.path.join(sw_base,"airelib/inc/logger.h"),"w") as f:
            f.write("#pragma once\n#include <string>\nvoid log_message(const std::string&);")
        with open(os.path.join(sw_base,"airelib/src/logger.cpp"),"w") as f:
            f.write('#include<iostream>\n#include"logger.h"\nvoid log_message(const std::string& m){std::cout<<"[LOG]"<<m<<std::endl;}')

    def _create_test_example(self, sw_base):
        with open(os.path.join(sw_base,"test/src/test_logger.cpp"),"w") as f:
            f.write('#include<gtest/gtest.h>\n#include"logger.h"\nTEST(LogTest,Msg){EXPECT_NO_THROW(log_message("Hi"));}')

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
            f.write("file(GLOB AIRWET_UART_SRC ${CMAKE_CURRENT_SOURCE_DIR}/aireWetUart/src/*.cpp)\n")
            f.write("file(GLOB AIRWET_MAIN_SRC ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)\n")
            f.write("file(GLOB AIRWET_TEST_SRC ${CMAKE_CURRENT_SOURCE_DIR}/test/src/*.cpp)\n\n")

            # Core UART library
            f.write("# Core UART library\n")
            f.write("add_library(airwet_uart STATIC ${AIRWET_UART_SRC})\n")
            f.write("target_include_directories(airwet_uart PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/aireWetUart/inc)\n\n")

            # Header-only wrapper
            f.write("# Header-only wrapper\n")
            f.write("add_library(airwet_libery INTERFACE)\n")
            f.write("target_include_directories(airwet_libery INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/aireLibery)\n\n")

            # Simulation mode
            f.write("# Simulation mode\n")
            f.write("if(BUILD_SIMULATION)\n")
            f.write("    add_executable(airwet_uart_sim ${AIRWET_MAIN_SRC})\n")
            f.write("    target_link_libraries(airwet_uart_sim PRIVATE airwet_uart airwet_libery)\n")
            f.write("    target_include_directories(airwet_uart_sim PRIVATE\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/aireWetUart/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/aireLibery\n")
            f.write("    )\n")
            f.write("endif()\n\n")

            # Product mode
            f.write("# Product mode\n")
            f.write("if(BUILD_PRODUCT)\n")
            f.write("    add_library(airwet_uart_shared SHARED ${AIRWET_UART_SRC})\n")
            f.write("    target_include_directories(airwet_uart_shared PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/aireWetUart/inc)\n")
            f.write("    set_target_properties(airwet_uart_shared PROPERTIES\n")
            f.write("        CXX_VISIBILITY_PRESET hidden\n")
            f.write("        VISIBILITY_INLINES_HIDDEN YES\n")
            f.write("    )\n")
            f.write("endif()\n\n")

            # Unit test mode
            f.write("# Unit test mode\n")
            f.write("if(BUILD_TESTS)\n")
            f.write("    find_package(GTest REQUIRED)\n")
            f.write("    enable_testing()\n\n")
            f.write("    add_executable(airwet_uart_tests ${AIRWET_TEST_SRC})\n")
            f.write("    target_include_directories(airwet_uart_tests PRIVATE\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/test/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/aireWetUart/inc\n")
            f.write("        ${CMAKE_CURRENT_SOURCE_DIR}/aireLibery\n")
            f.write("    )\n")
            f.write("    target_link_libraries(airwet_uart_tests PRIVATE\n")
            f.write("        airwet_uart\n")
            f.write("        airwet_libery\n")
            f.write("        GTest::gtest\n")
            f.write("        GTest::gtest_main\n")
            f.write("    )\n\n")
            f.write("    include(GoogleTest)\n")
            f.write("    gtest_discover_tests(airwet_uart_tests)\n")
            f.write("endif()\n\n")

            # End of file marker
            f.write("# End of CMakeLists.txt\n")

        print(f"CMakeLists.txt written to {cmake_path}")

