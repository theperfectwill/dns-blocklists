# ---------------------------------
# Script Name: RemoveRedundancy.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/RemoveRedundancy.py
# --i _Input_File_ --p {phrase_to_remove} --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

# Core
from pathlib import Path
import argparse
import logging
import os
import re
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

DEFAULT_NAMES_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Names"
DEFAULT_NUMERICAL_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Numerical"
DEFAULT_SPACED_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Spaced"
DEFAULT_KEYWORDS_FILE = Path(Data.NSFW_PATH) / "filterize.txt"

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

def setup_logging(logging_level: str = "INFO") -> None:
    logging.basicConfig(level=logging_level, **Data.LOG)

def validate_input_file(input_file: str) -> None:
    if not Path(input_file).is_file():
        logging.error(f"The input file '{input_file}' does not exist.")
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

def validate_output_directory(output_dir: str) -> None:
    if not Path(output_dir).is_dir():
        logging.error(f"The output directory '{output_dir}' does not exist.")
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist.")

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def remove_lines_with_phrases_in_directory(directory_path, phrases_file_path):
    # Validate the directory path
    if not os.path.isdir(directory_path):
        logging.error(f"The directory '{directory_path}' is not valid.")
        return

    # Validate the phrases file path
    if not os.path.isfile(phrases_file_path):
        logging.error(f"The phrases file '{phrases_file_path}' is not valid.")
        return

    try:
        # Read the phrases from the specified file, ignoring lines starting with "!"
        with open(phrases_file_path, 'r') as phrases_file:
            phrases = {line.strip() for line in phrases_file if not line.startswith("!")}

        # List all files in the directory and sort them alphabetically
        files = sorted(os.listdir(directory_path))
        total_files_processed = 0
        total_lines_removed = 0

        for file_name in files:
            file_path = os.path.join(directory_path, file_name)

            # Check if the path is a file
            if os.path.isfile(file_path):
                # Read the contents of the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Filter out lines that contain any of the specified phrases
                filtered_lines = [line for line in lines if not any(phrase in line for phrase in phrases)]
                lines_removed = len(lines) - len(filtered_lines)
                total_lines_removed += lines_removed

                # Write the filtered lines back to the file only if changes were made
                if lines_removed > 0:
                    with open(file_path, 'w') as file:
                        file.writelines(filtered_lines)
                    logging.info(f"Removed {lines_removed} lines containing phrases from '{phrases_file_path}' in '{file_path}'.")
                    total_files_processed += 1

        logging.info(f"Processed {total_files_processed} files. Total lines removed: {total_lines_removed}.")

    except PermissionError:
        logging.error(f"Permission denied when trying to access '{directory_path}' or '{phrases_file_path}'.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Remove lines containing specified phrases from files in a directory.")
    parser.add_argument('--d', type=str, help='Path to the directory containing files.')
    parser.add_argument('--pf', type=str, help='Path to the file containing phrases to filter out.')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    if not args.d or not args.pf:
        if not args.d:
            args.d = input("Please enter the path to the directory containing files to remove phrases from: ")
        if not args.pf:
            args.pf = input("Please enter the path to the file containing phrases to filter by: ")

    # remove_lines_with_phrase(args.i, args.phrase_file)
    # remove_lines_with_phrase(DEFAULT_NAMES_PATH, DEFAULT_KEYWORDS_FILE)
    # remove_lines_with_phrase(DEFAULT_NUMERICAL_PATH, DEFAULT_KEYWORDS_FILE)
    remove_lines_with_phrase(DEFAULT_SPACED_PATH, DEFAULT_KEYWORDS_FILE)

    remove_lines_with_phrases_in_directory(args.d, args.pf)

if __name__ == "__main__":
    main()
