# ---------------------------------
# Script Name: Code/Scripts/AlphabeticalCommon.py
# Version: 1.0.0.0
# Description: This script reads text files, counts the occurrences of patterns, and writes the most common patterns to output files.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/AlphabeticalCommon.py
# --i _Input_File_ --max_patterns 1000 --min_length 3 --max_length 64 --ll ERROR
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

EXTRACTS_TXT = "extracts.txt"
COMMON_TXT = "common.txt"
EXCLUSIONS_TXT = "exclusions.txt"

DEFAULT_OUTPUT_FILE = "common.txt"
DEFAULT_MAX_PATTERNS = 3000
DEFAULT_MIN_LENGTH = 4
DEFAULT_MAX_LENGTH = 64

DEFAULT_MIN_ONLY_NUMBERS_LENGTH = 5
DEFAULT_ONLY_NUMBERS_NUM_COMMON = 50

TASKS = [
    # Special
    (f"{Data.SORTED_PATH}/DomainParents/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/DomainParents/{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/DomainChildren/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/DomainChildren/{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Conjoined/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/Conjoined/{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/OnlyLetters/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/OnlyLetters/{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/OnlyNumbers/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/OnlyNumbers/{COMMON_TXT}", DEFAULT_ONLY_NUMBERS_NUM_COMMON, DEFAULT_MIN_ONLY_NUMBERS_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/WildCards/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/WildCards/{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    # Alphabetical
    (f"{Data.SORTED_PATH}/Alphabetical/A.txt", f"{Data.SORTED_PATH}/Alphabetical/A.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/B.txt", f"{Data.SORTED_PATH}/Alphabetical/B.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/C.txt", f"{Data.SORTED_PATH}/Alphabetical/C.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/D.txt", f"{Data.SORTED_PATH}/Alphabetical/D.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/E.txt", f"{Data.SORTED_PATH}/Alphabetical/E.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/F.txt", f"{Data.SORTED_PATH}/Alphabetical/F.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/G.txt", f"{Data.SORTED_PATH}/Alphabetical/G.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/H.txt", f"{Data.SORTED_PATH}/Alphabetical/H.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/I.txt", f"{Data.SORTED_PATH}/Alphabetical/I.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/J.txt", f"{Data.SORTED_PATH}/Alphabetical/J.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/K.txt", f"{Data.SORTED_PATH}/Alphabetical/K.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/L.txt", f"{Data.SORTED_PATH}/Alphabetical/L.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/M.txt", f"{Data.SORTED_PATH}/Alphabetical/M.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/N.txt", f"{Data.SORTED_PATH}/Alphabetical/N.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/O.txt", f"{Data.SORTED_PATH}/Alphabetical/O.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/P.txt", f"{Data.SORTED_PATH}/Alphabetical/P.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Q.txt", f"{Data.SORTED_PATH}/Alphabetical/Q.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/R.txt", f"{Data.SORTED_PATH}/Alphabetical/R.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/S.txt", f"{Data.SORTED_PATH}/Alphabetical/S.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/T.txt", f"{Data.SORTED_PATH}/Alphabetical/T.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/U.txt", f"{Data.SORTED_PATH}/Alphabetical/U.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/V.txt", f"{Data.SORTED_PATH}/Alphabetical/V.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/W.txt", f"{Data.SORTED_PATH}/Alphabetical/W.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/X.txt", f"{Data.SORTED_PATH}/Alphabetical/X.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Y.txt", f"{Data.SORTED_PATH}/Alphabetical/Y.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Z.txt", f"{Data.SORTED_PATH}/Alphabetical/Z.{COMMON_TXT}", DEFAULT_MAX_PATTERNS, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
]

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

def get_common_character_patterns(input_file: str, output_file: str, max_patterns: int = 1000, min_length: int = 3, max_length: int = float('inf')) -> Optional[Counter]:
    # Validate parameters
    if max_patterns <= 0:
        logging.error("Parameter 'max_patterns' must be greater than 0.")
        return None
    if min_length < 1 or max_length < min_length:
        logging.error("Invalid length parameters: min_length must be >= 1 and max_length must be >= min_length.")
        return None

    # Validate and create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created directory: {output_dir}")
        except OSError as e:
            logging.error(f"Failed to create directory {output_dir}: {e}")
            return None

    try:
        # Read exclusions from the specified file
        exclusions = set()
        with open(f"{Data.RULES_PATH}/{EXCLUSIONS_TXT}", 'r', encoding='utf-8') as exclusions_file:
            for line in exclusions_file:
                line = line.strip()
                if line and not line.startswith("!"):  # Skip empty lines and lines starting with "!"
                    exclusions.add(line)

        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Normalize content to lowercase
        content = content.lower()

        # Extract character patterns of specified lengths
        # Patterns of any kind...
        # patterns = re.findall(r'.{%d,%d}' % (min_length, max_length), content)  # Match patterns of length min_length to max_length
        # Letter patterns only
        # patterns = re.findall(r'[a-z]{%d,%d}' % (min_length, max_length), content)  # Match patterns of length min_length to max_length
        # Detects Repeating Characters By {2} Minimum
        # patterns = re.findall(r'(\w{2})\1{1,}{%d,%d}' % (min_length, max_length), content)  # Match patterns of length min_length to max_length
        # Detects lines that start with a digit
        patterns = re.findall(r'^\d.*$', content, re.MULTILINE)

        logging.info(f"Total patterns found: {len(patterns)}")

        # Count occurrences of each pattern
        pattern_counts = Counter(patterns)

        # Remove any patterns that are in the exclusions set
        for pattern in list(pattern_counts.keys()):
            if pattern in exclusions:
                del pattern_counts[pattern]

        logging.info(f"Excluded patterns: {len(pattern_counts)}")

        # Get the most common patterns
        common_patterns = pattern_counts.most_common(max_patterns)

        with open(output_file, 'w', encoding='utf-8') as file:
            for pattern, count in common_patterns:
                file.write(f"{count}: {pattern}\n")

        return pattern_counts  # Return the pattern counts as a Counter

    except FileNotFoundError:
        logging.error(f"The file {input_file} was not found.")
    except IOError as e:
        logging.error(f"An IOError occurred: {e}")

    return None

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Analyze text for common character patterns.')
    parser.add_argument('--i', '--input_file', type=str, default=DEFAULT_INPUT_FILE, help='Input text file (default: sourceLinks.txt)')
    parser.add_argument('--o', '--output_file', type=str, default=DEFAULT_OUTPUT_FILE, help='Output file for common patterns (default: common_patterns.txt)')
    parser.add_argument('--max_patterns', type=int, default=DEFAULT_MAX_PATTERNS, help='Number of common patterns to retrieve (default: 1000)')
    parser.add_argument('--min_length', type=int, default=DEFAULT_MIN_LENGTH, help='Minimum length of patterns (default: 3)')
    parser.add_argument('--max_length', type=int, default=DEFAULT_MAX_LENGTH, help='Maximum length of patterns (default: 64)')
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

    # Check if no arguments were passed (i.e., defaults are used)
    if (args.i == DEFAULT_INPUT_FILE and
        args.o == DEFAULT_OUTPUT_FILE and
        args.max_patterns == DEFAULT_MAX_PATTERNS and
        args.min_length == DEFAULT_MIN_LENGTH and
        args.max_length == DEFAULT_MAX_LENGTH):

        # Process each task in TASKS
        for input_file, output_file, max_patterns, min_length, max_length in TASKS:
            pattern_counts = get_common_character_patterns(input_file, output_file, max_patterns, min_length, max_length)
            if pattern_counts is not None:
                logging.info(f"Processed {len(pattern_counts)} common patterns from {input_file}")
                logging.info(f"Added maximum of {max_patterns} common patterns to {output_file}")
                print()
    else:
        # Call the routine with the provided arguments
        pattern_counts = get_common_character_patterns(args.i, args.o, args.max_patterns, args.min_length, args.max_length)
        if pattern_counts is not None:
            logging.info(f"Processed {len(pattern_counts)} common patterns from {args.i}")
            logging.info(f"Added maximum of {args.max_patterns} common patterns to {args.o}")
            print()

if __name__ == "__main__":
    main()
