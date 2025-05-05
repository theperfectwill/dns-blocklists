# ---------------------------------
# Script Name: CombinePatternRules.py
# Version: 1.0.0.0
# Description: This code combines filtered patterns from a specified strings file and regex file into a single output file
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/CombinePatternRules.py
# --i _Input_File_ --r _Regex_File_ --o _Output_Path_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from pathlib import Path
from typing import List
import argparse
import logging
import os
import re
import sys
import traceback

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our constants
# ---------------------------------

STRINGS_TXT = Path(Data.RULES_PATH) / "strings.txt"
REGEX_TXT = Path(Data.RULES_PATH) / "regex.txt"
COMBINED_TXT = Path(Data.RULES_PATH) / "combined.txt"

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
# SECTION: Define our functions
# ---------------------------------

def read_filtered_lines(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        logging.error(f"Error: The file '{file_path}' does not exist.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [
                line.strip() for line in file
                if line.strip() and not line.startswith("!")
            ]
            logging.info(f"Successfully read {len(lines)} filtered lines from '{file_path}'.")
            return lines
    except Exception as e:
        logging.error(f"An error occurred while reading '{file_path}': {e}\n{traceback.format_exc()}")
        return []

def filter_special_characters(patterns: List[str]) -> List[str]:
    filtered_patterns = [
        re.sub(r'[^a-zA-Z0-9\s-]', '', pattern)
        for pattern in patterns
    ]
    logging.info(f"Filtered special characters from {len(patterns)} wildcard patterns.")
    return filtered_patterns

def write_combined_patterns(strings_file: str, regex_file: str, output_file: str) -> None:
    string_results = read_filtered_lines(strings_file)
    regex_results = read_filtered_lines(regex_file)

    filtered_strings = filter_special_characters(string_results)

    # Use a set for faster membership testing
    filtered_string_set = set(filtered_strings)

    # Start with string_results in combined_results
    combined_results = string_results.copy()

    # Add regex patterns that do not match any filtered string patterns
    combined_results.extend(
        regex for regex in regex_results
        if not any(filtered_string in regex for filtered_string in filtered_string_set)
    )

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created directory '{output_dir}' for output file.")
        except Exception as e:
            logging.error(f"An error occurred while creating directory '{output_dir}': {e}\n{traceback.format_exc()}")
            return

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(combined_results) + '\n')
        logging.info(f"{len(combined_results)} combined patterns written to '{output_file}'.")
    except Exception as e:
        logging.error(f"An error occurred while writing to '{output_file}': {e}\n{traceback.format_exc()}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Combine pattern rules from strings and regex files.')
    parser.add_argument('--i', '--input_file', type=str, default=STRINGS_TXT, help='Path to the input strings file.')
    parser.add_argument('--r', '--regex_file', type=str, default=REGEX_TXT, help='Path to the regex patterns file.')
    parser.add_argument('--o', '--output_file', type=str, default=COMBINED_TXT, help='Path to the output combined file.')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    # Validate our inputs and outputs
    validate_input_file(args.i)
    # validate_output_directory(args.o)

    # Now call any routines
    write_combined_patterns(args.i, args.r, args.o)

if __name__ == "__main__":
    main()
