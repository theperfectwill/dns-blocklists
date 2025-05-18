# ---------------------------------
# Script Name: RemoveRedundancy.py
# Version: 1.0.0.0
# Description: The function format_file formats/strips a blocklist to our liking
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
DEFAULT_KEYWORDS_FILE = Path(Data.NSFW_PATH) / "manualKeywords.txt"

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
    try:
        # Read the phrases from the specified file, ignoring lines starting with "!"
        with open(phrases_file_path, 'r') as phrases_file:
            phrases = [line.strip() for line in phrases_file.readlines() if not line.startswith("!")]

        # List all files in the directory and sort them alphabetically
        files = sorted(os.listdir(directory_path))

        for file_name in files:
            file_path = os.path.join(directory_path, file_name)

            # Check if the path is a file
            if os.path.isfile(file_path):
                # Read the contents of the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Filter out lines that contain any of the specified phrases
                filtered_lines = [line for line in lines if not any(phrase in line for phrase in phrases)]

                # Write the filtered lines back to the file
                with open(file_path, 'w') as file:
                    file.writelines(filtered_lines)

                print(f"Lines containing phrases from '{phrases_file_path}' have been removed from '{file_path}'.")

    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' or phrases file '{phrases_file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{directory_path}' or '{phrases_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    # Define logging settings
    setup_logging(args.ll)

    # remove_lines_with_phrase(args.i, args.phrase_file)
    remove_lines_with_phrase(DEFAULT_NAMES_PATH, DEFAULT_KEYWORDS_FILE)
    # remove_lines_with_phrase(DEFAULT_NUMERICAL_PATH, DEFAULT_KEYWORDS_FILE)
    remove_lines_with_phrase(DEFAULT_SPACED_PATH, DEFAULT_KEYWORDS_FILE)

if __name__ == "__main__":
    main()
