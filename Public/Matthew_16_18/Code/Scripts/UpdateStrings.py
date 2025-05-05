# ---------------------------------
# Script Name: UpdateStrings.py
# Version: 1.0.0.0
# Description: Update strings in file contents and directory names within the specified root directory.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/UpdateStrings.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from pathlib import Path
import logging
import shutil
import sys
import argparse
import os

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

def setup_logging(logging_level: str = "INFO") -> None:
    logging.basicConfig(level=logging_level, **Data.LOG)

def validate_input_file(input_file: Path) -> None:
    if not input_file.is_file():
        logging.error(f"The input file '{input_file}' does not exist.")
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

def validate_output_directory(output_dir: Path) -> None:
    if not output_dir.is_dir():
        logging.error(f"The output directory '{output_dir}' does not exist.")
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist.")

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

FILES_RENAMED = 'files_renamed'
DIRECTORIES_RENAMED = 'directories_renamed'

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def update_old_strings_to_new_strings(directory: Path, old_string: str, new_string: str) -> dict:
    directory_path = Path(directory)

    if not directory_path.exists():
        logging.error(f'The directory {directory} does not exist.')
        return {FILES_RENAMED: 0, DIRECTORIES_RENAMED: 0}

    if not directory_path.is_dir():
        logging.error(f'The path {directory} is not a directory.')
        return {FILES_RENAMED: 0, DIRECTORIES_RENAMED: 0}

    if not old_string or not new_string:
        logging.error('old_string and new_string must not be empty.')
        return {FILES_RENAMED: 0, DIRECTORIES_RENAMED: 0}

    if old_string == new_string:
        logging.info('No changes made as old_string is the same as new_string.')
        return {FILES_RENAMED: 0, DIRECTORIES_RENAMED: 0}

    files_renamed = 0
    directories_renamed = 0

    # Check if the directory is empty
    if not any(directory_path.iterdir()):
        logging.info(f'The directory {directory} is empty. No files or directories to rename.')
        return {FILES_RENAMED: 0, DIRECTORIES_RENAMED: 0}

    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for dirname in dirnames:
                if old_string in dirname:
                    old_dir_path = Path(dirpath) / dirname
                    new_dirname = dirname.replace(old_string, new_string)
                    new_dir_path = Path(dirpath) / new_dirname

                    try:
                        old_dir_path.rename(new_dir_path)
                        logging.info(f'Renamed directory: {old_dir_path} to {new_dir_path}')
                        directories_renamed += 1
                    except (FileNotFoundError, PermissionError) as e:
                        logging.error(f'Error renaming directory {old_dir_path}: {e}')

            for filename in filenames:
                old_file_path = Path(dirpath) / filename
                file_updated = False

                # Update file name if old_string is found
                if old_string in filename:
                    new_filename = filename.replace(old_string, new_string)
                    new_file_path = Path(dirpath) / new_filename

                    try:
                        old_file_path.rename(new_file_path)
                        logging.info(f'Renamed file: {old_file_path} to {new_file_path}')
                        files_renamed += 1
                        old_file_path = new_file_path  # Update the path for content modification
                    except (FileNotFoundError, PermissionError) as e:
                        logging.error(f'Error renaming file {old_file_path}: {e}')

                # Read and update file content in binary mode
                try:
                    with open(old_file_path, 'rb') as file:
                        content = file.read()

                    # Perform byte-level replacement
                    old_bytes = old_string.encode('utf-8')
                    new_bytes = new_string.encode('utf-8')
                    if old_bytes in content:
                        updated_content = content.replace(old_bytes, new_bytes)
                        with open(old_file_path, 'wb') as file:
                            file.write(updated_content)
                        logging.info(f'Updated content in file: {old_file_path}')
                        file_updated = True

                except (FileNotFoundError, PermissionError) as e:
                    logging.error(f'Error processing file {old_file_path}: {e}')

                if file_updated:
                    files_renamed += 1  # Count the content update as a rename

    except Exception as e:
        logging.error(f'Error processing directory {directory}: {e}')

    return {FILES_RENAMED: files_renamed, DIRECTORIES_RENAMED: directories_renamed}

# ---------------------------------
# SECTION: Command-Line Argument Parsing
# ---------------------------------

# @Todo->add this to common style of coding then call in main()
def get_user_input() -> (Path, str, str):
    directory = input("Enter the root directory: ")
    old_string = input("Enter the string to be replaced: ")
    new_string = input("Enter the new string: ")
    return Path(directory), old_string, new_string

# @Todo->add this to common style of coding then call in main()
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update strings in file contents and directory names.")
    parser.add_argument("root_dir", type=str, help="The root directory to search for updates.")
    parser.add_argument("old_string", type=str, help="The string to be replaced.")
    parser.add_argument("new_string", type=str, help="The new string to replace with.")
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )
    return parser.parse_args()

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # args = parse_arguments()
    directory, old_string, new_string = get_user_input()

    # Define logging settings
    setup_logging()

    # Validate our inputs and outputs
    # validate_input_file(args.i)
    validate_output_directory(directory)
    
    # Now call any routines
    update_old_strings_to_new_strings(directory, old_string, new_string)

if __name__ == "__main__":
    main()
