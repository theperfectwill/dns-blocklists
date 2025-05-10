# ---------------------------------
# Script Name: Code/Scripts/RemoveDuplicateWords.py
# Version: 1.0.0.0
# Description: This script finds words that exist in one line and removes them if they exist in another line, effectively reducing a file to single unique words.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/RemoveDuplicateWords.py
# --i _Input_File_ --o _Output_File_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from collections import Counter
from pathlib import Path
from typing import Optional, List
import argparse
import logging
import os
import re
import subprocess
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

DEFAULT_INPUT_FILE = Path(Data.SOURCES_PATH) / "blocklist.txt"
DEFAULT_OUTPUT_FILE = Path(Data.NSFW_PATH) / "blocklist.txt"

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

def remove_common_words(input_file: str, output_file: str) -> int:
    # Read the input file and store lines
    try:
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
    except IOError as e:
        logging.error(f"Error reading file {input_file}: {e}")
        raise

    # Create a Counter to count occurrences of each word
    word_counts = Counter(word for line in lines for word in line.split())

    # Create a list to store modified lines
    modified_lines = []

    # Remove common words from each line
    for line in lines:
        words = line.split()
        # Create a new list of words that are not in the set of all words
        unique_words = [word for word in words if word_counts[word] == 1]
        modified_lines.append(' '.join(unique_words))

    # Write the modified lines to the output file
    try:
        with open(output_file, 'w') as file:
            for line in modified_lines:
                if line:  # Ensure it's not an empty line
                    file.write(line + '\n')
    except IOError as e:
        logging.error(f"Error writing to file {output_file}: {e}")
        raise

    return len(modified_lines)  # Return the count of modified lines

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Analyze text for common character patterns.')
    parser.add_argument('--i', '--input_file', type=str, default=DEFAULT_INPUT_FILE, help='Input text file (default: blocklist.txt)')
    parser.add_argument('--o', '--output_file', type=str, default=DEFAULT_OUTPUT_FILE, help='Output file for unique words (default: blocklist.txt)')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    # Validate our inputs
    validate_input_file(args.i)

    # Call the routine with the provided arguments
    unique_word_count = remove_common_words(args.i, args.o)
    logging.info(f"Processed {unique_word_count} unique words from {args.i} to {args.o}")

if __name__ == "__main__":
    main()
