# ---------------------------------
# Script Name: StringUpdates.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
import logging
import os
import shutil
import sys

# Helpers

# Custom
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Scripts'))
import _Vars

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**_Vars.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def update_folder_strings(root_dir, old_string, new_string):
    if not os.path.isdir(root_dir):
        logging.error(f"The specified root directory does not exist: {root_dir}")
        return

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Update files
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                if old_string in content:
                    new_content = content.replace(old_string, new_string)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    logging.info(f"Updated file: {file_path}")
            except (IOError, OSError) as e:
                logging.error(f"Error processing file: {file_path} - {e}")

        # Update directories
        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            if old_string in dirname:
                new_dirname = dirname.replace(old_string, new_string)
                new_dir_path = os.path.join(dirpath, new_dirname)
                if new_dir_path != dir_path:  # Avoid renaming to the same name
                    try:
                        shutil.move(dir_path, new_dir_path)
                        logging.info(f"Updated directory: {dir_path} -> {new_dir_path}")
                    except (IOError, OSError, shutil.Error) as e:
                        logging.error(f"Error processing directory: {dir_path} - {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    update_folder_strings(os.getcwd(), 'ThisFolderName', _Vars.FOLDER_NAME)

if __name__ == "__main__":
    main() 
