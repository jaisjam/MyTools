#!/usr/bin/env python3
import os
from AIRXX_aireWetICEgenBase import IceGen

class IceGenSw(IceGen):
    def create_sw_structure(self, base):
        sw_base = os.path.join(base, "software")
        os.makedirs(sw_base, exist_ok=True)
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

    def _write_sw_cmakelists(self, sw_base):
        with open(os.path.join(sw_base,"CMakeLists.txt"),"w") as f:
            f.write("cmake_minimum_required(VERSION 3.16)\nproject(fpga_platform CXX)\nenable_testing()\nset(CMAKE_CXX_STANDARD 17)\n")
            f.write("add_executable(fpga_platform main.cpp airelib/src/logger.cpp)\n")
            f.write("target_include_directories(fpga_platform PRIVATE airelib/inc module/inc)\n")
            f.write("find_package(GTest REQUIRED)\nadd_executable(runTests test/src/test_logger.cpp airelib/src/logger.cpp)\n")
            f.write("target_include_directories(runTests PRIVATE airelib/inc module/inc)\n")
            f.write("target_link_libraries(runTests GTest::GTest GTest::Main pthread)\nadd_test(NAME runTests COMMAND runTests)\n")
