# ---------------------------------
# Script Name: ImportSorted.py
# Version: 1.0.0.0
# Description: Imports NSFW keywords and profile names into combined{X}.txt with our desired adblock formatting.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/ImportSorted.py
# --i _Input_Path_ --o _Output_Path_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from collections import defaultdict
from pathlib import Path
import argparse
import glob
import logging
import re
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our constants
# ---------------------------------

DEFAULT_NAMES_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Names" / "*.txt"
DEFAULT_NUMERICAL_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Numerical" / "*.txt"
DEFAULT_SPACED_PATH = Path(Data.NSFW_PATH) / "Keywords" / "Spaced" / "*.txt"

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

def setup_logging(logging_level: str = "INFO") -> None:
    logging.basicConfig(level=logging_level, **Data.LOG)

def validate_input_file(input_file: str) -> None:
    if not Path(input_file).is_file():
        logging.error(f"The input file '{input_file}' does not exist.")
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

def validate_directory(output_dir: str) -> None:
    if not Path(output_dir).is_dir():
        logging.error(f"The output directory '{output_dir}' does not exist.")
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist.")

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def extract_nsfw_patterns() -> None:
    try:
        # Function to read files and write combined output
        def read_and_combine_files(input_path, output_file):
            combined_lines = []
            # Get a sorted list of file paths
            file_paths = sorted(glob.glob(str(input_path)))
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        combined_lines.extend(lines)
                except IOError as e:
                    logging.error(f"Error reading file {file_path}: {e}")

            # Write combined lines to output file
            with open(output_file, 'w', encoding='utf-8') as outfile:
                modified_lines = [line.replace(' ', '*').replace('.', '*') for line in combined_lines]
                outfile.writelines(modified_lines)

        # Process each category
        read_and_combine_files(Path(Data.NSFW_PATH) / "Keywords/Spaced/*.txt", Path(Data.NSFW_PATH) / "combinedSpaced.txt")
        read_and_combine_files(Path(Data.NSFW_PATH) / "Keywords/Names/*.txt", Path(Data.NSFW_PATH) / "combinedNames.txt")
        read_and_combine_files(Path(Data.NSFW_PATH) / "Keywords/Numerical/*.txt", Path(Data.NSFW_PATH) / "combinedNumerical.txt")
        read_and_combine_files(Path(Data.NSFW_PATH) / "Keywords/Single/*.txt", Path(Data.NSFW_PATH) / "combinedSingle.txt")

        # Combine all results into a single file
        combined_all = []
        for combined_file in [
                Path(Data.NSFW_PATH) / 'combinedSpaced.txt',
                Path(Data.NSFW_PATH) / 'combinedNames.txt',
                Path(Data.NSFW_PATH) / 'combinedNumerical.txt',
                Path(Data.NSFW_PATH) / 'combinedSingle.txt'
            ]:
            try:
                with open(combined_file, 'r', encoding='utf-8') as file:
                    combined_all.extend(file.readlines())
            except IOError as e:
                logging.error(f"Error reading {combined_file}: {e}")

        # Write all combined lines to NSFW/combined.txt
        with open(Path(Data.NSFW_PATH) / 'combined.txt', 'w', encoding='utf-8') as outfile:
            outfile.writelines(combined_all)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Analyze text for common character patterns.')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    # Now call any routines
    extract_nsfw_patterns()

if __name__ == "__main__":
    main()