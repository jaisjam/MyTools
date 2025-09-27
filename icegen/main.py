#!/usr/bin/env python3

import os
from AIRXX_aireWetICEgenBase import IceGen
from AIRXX_aireWetICEgenHardWare import IceGenHw
from AIRXX_aireWetICEgenSoftWare import IceGenSw

def main():
    base = IceGen()
    args = base.parse_args()
    project, device, template = args.project, args.device, args.template
    top = template if template!="none" else project
    base_dir = os.path.abspath(project)
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir,"build"), exist_ok=True)
    IceGenHw().create_hw_structure(base_dir, device, top, template)
    IceGenSw().create_sw_structure(base_dir)
    base.write_root_cmakelists(base_dir, project)
    base.write_root_readme(base_dir, project)
    print(f"✅ Project '{project}' created")

if __name__=="__main__": main()
