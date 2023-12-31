#!/usr/bin/python3

import os, sys

# returns the path to the desired directory
def prompt_path_to_dir():
    # len includes argv[0] (i.e. the name of the script)
    if len(sys.argv) < 2:
        in_ = input("Please specify path to folder (use \"\" for current folder)\n").strip()

        if in_.find("\"") == 0:
            in_ = in_[1:len(in_) - 1]
        
        if in_ != "":
            return in_
        else:
            return "."
    else:
        return sys.argv[1]

def extrude(dir_path):
    dir_parent = dir_path

    def extrude_inner(dir_path):
        for thing in os.listdir(dir_path):
            path_full_local = os.path.join(dir_path, thing)
            if os.path.isdir(path_full_local):
                extrude_inner(path_full_local)
                os.rmdir(path_full_local)
            else:
                os.rename(path_full_local, os.path.join(dir_parent, thing))
    
    extrude_inner(dir_path)

    input("\nMoving complete. Press ENTER to close.")
    

# ----------------- Main ------------------------
print("----- Extruder v1 -----\n")
extrude(dir_path = prompt_path_to_dir())