#!/usr/bin/python3

import os, re, sys

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
    
def prompt_replacement_string():
    # len includes argv[0] (i.e. the name of the script)
    if len(sys.argv) < 3:
        in_ = input("\nPlease specify base string.\nEx: \"img_\" = \"photo23\" -> \"img_23\"\n\"img_\" is the default string.\n")
        
        if in_ != "":
            return in_
        else:
            return "img_"
    else:
        return sys.argv[2]
    
def prompt_keep_original_numbers():
    in_ = input("\nWould you like to keep the numbers that already exist in the names? Y/n\n")

    return in_[0:1].upper() == "Y"
        
        
# All from https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# Creates a list with all files in "natural order"
# Helper function for rename().
# os.path.isfile() from https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
def _files_only(dirPath):
    return_list = []

    for thing in os.listdir(dirPath):
        if os.path.isfile(os.path.join(dirPath, thing)):
            return_list.append(thing)
    
    return_list.sort(key=natural_keys)

    return return_list

# Reverses string; finds period; outputs extension with "."
# Helper function for rename().
def _return_exetension(string: str):
    index = string[::-1].find(".")

    if index < 0:
        return ""
    else:
        return string[-index - 1:]
    
# Finds the numbers that already exist in the string and return them.
# Helper function for rename().
# isalpha() from https://www.w3schools.com/python/ref_string_isalpha.asp
def _return_existing_numbers(string: str):
    # removes extension
    base_string = string[0: -string[::-1].find(".") - 1]
    reverse_base_string = base_string[::-1]

    start = 0
    end = len(base_string)
    
    # Assumes the numbers are at the end.
    # Stops on first number.
    for char in reverse_base_string:
        if char.isnumeric():
            break
        else:
            end -= 1
    
    start = end

    # Continues from end varible.
    # Stops on first non-number.
    for char in reverse_base_string[-end:]:
        if not char.isnumeric():
            break
        else:
            start -= 1

    # If there are no numbers, start = end = 0.
    return base_string[start:end]


# Only pass the directory path and string.
def rename(dirPath, repStr):
    dir = _files_only(dirPath)
    count = 1

    if prompt_keep_original_numbers():
        for file in dir:
            os.rename(os.path.join(dirPath, file), os.path.join(dirPath, repStr + _return_existing_numbers(file) + _return_exetension(file)))
    else:
        for file in dir:
            os.rename(os.path.join(dirPath, file), os.path.join(dirPath, repStr + str(count).zfill(len(str(len(dir)))) + _return_exetension(file)))
            count += 1


    input("\nRenaming complete. Press ENTER to close.")
    

# ----------------- Main ------------------------
print("----- Renamer v2 -----\n")
rename(dirPath = prompt_path_to_dir(), repStr = prompt_replacement_string())

