#!/usr/bin/env python3

import os
import sys
import argparse
import platform
from datetime import datetime
from AIRXX_aireWetICEgenBase import IceGen
from AIRXX_aireWetICEgenHardWare import IceGenHw
from AIRXX_aireWetICEgenSoftWare import IceGenSw

VERSION = "0.0.01"
ORGANIZATION = "aireWet"

# Collect environment info once
_prog = "icegen"
_python_ver = platform.python_version()
_system = platform.system()
_release = platform.release()
_build_date = datetime.now().strftime("%Y-%m-%d")

HELP_TEXT = """Usage: icegen [options]
Options:
  -p <project>, --project <project>   Project name (directory will be created if not exists).
  -t <template>, --template <template>
                                      Template to use for the project (or 'none').
  -d <device>, --device <device>      Target FPGA device (e.g., iCEBreaker v1.0e, up5k).
  -h, --help                          Display this information.
  -v, --version                       Display version information.

Examples:
  icegen -p blink -t sample -d up5k
  icegen --project demo --device iCEBreaker
"""

VERSION_TEXT = f"""{_prog} {VERSION} ({_system} {_release}) built {_build_date}
Copyright (C) 2025 {ORGANIZATION}
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Built with Python {_python_ver} on {_system} {_release}
"""

def parse_arguments():
    parser = argparse.ArgumentParser(add_help=False)  # no default help
    parser.add_argument("-p", "--project", help="Project name")
    parser.add_argument("-d", "--device", default="iCEBreaker", help="FPGA device")
    parser.add_argument("-t", "--template", default="none", help="Template")
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.help:
        print(HELP_TEXT)
        sys.exit(0)

    if args.version:
        print(VERSION_TEXT)
        sys.exit(0)

    if not args.project:
        print("icegen: error: the following argument is required: -p/--project")
        print("Try 'icegen --help' for more information.")
        sys.exit(1)

    return args

def main():
    args = parse_arguments()
    project, device, template = args.project, args.device, args.template
    top = template if template != "none" else project
    base_dir = os.path.abspath(project)

    # Ensure directories exist
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "build"), exist_ok=True)

    # Generate hardware + software structure
    base = IceGen()
    IceGenHw().create_hw_structure(base_dir, device, top, template)
    IceGenSw().create_sw_structure(base_dir)

    # Write build + readme files
    base.write_root_build(base_dir, project)
    base.write_root_readme(base_dir, project)

    print(f"✅ Project '{project}' created at {base_dir}")

if __name__ == "__main__":
    main()
