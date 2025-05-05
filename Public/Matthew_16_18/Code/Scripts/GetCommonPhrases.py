# ---------------------------------
# Script Name: Code/Scripts/GetCommonPhrases.py
# Version: 1.0.0.0
# Description: This script reads text files, counts the occurrences of phrases, and writes the most common phrases to output files.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/GetCommonPhrases.py
# --i _Input_File_ --max_phrases 1000 --min_length 3 --max_length 64 --ll ERROR
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

DEFAULT_MAX_PHRASES = 1000
DEFAULT_MIN_LENGTH = 3
DEFAULT_MAX_LENGTH = 64

DEFAULT_MIN_ONLY_NUMBERS_LENGTH = 5
DEFAULT_ONLY_NUMBERS_NUM_COMMON = 50

TASKS = [
    # Special
    (f"{Data.SORTED_PATH}/DomainParents/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/DomainParents/{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/DomainChildren/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/DomainChildren/{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Conjoined/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/Conjoined/{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/OnlyLetters/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/OnlyLetters/{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/OnlyNumbers/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/OnlyNumbers/{COMMON_TXT}", DEFAULT_ONLY_NUMBERS_NUM_COMMON, DEFAULT_MIN_ONLY_NUMBERS_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/WildCards/{EXTRACTS_TXT}", f"{Data.SORTED_PATH}/WildCards/{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    # Alphabetical
    (f"{Data.SORTED_PATH}/Alphabetical/A.txt", f"{Data.SORTED_PATH}/Alphabetical/A.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/B.txt", f"{Data.SORTED_PATH}/Alphabetical/B.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/C.txt", f"{Data.SORTED_PATH}/Alphabetical/C.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/D.txt", f"{Data.SORTED_PATH}/Alphabetical/D.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/E.txt", f"{Data.SORTED_PATH}/Alphabetical/E.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/F.txt", f"{Data.SORTED_PATH}/Alphabetical/F.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/G.txt", f"{Data.SORTED_PATH}/Alphabetical/G.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/H.txt", f"{Data.SORTED_PATH}/Alphabetical/H.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/I.txt", f"{Data.SORTED_PATH}/Alphabetical/I.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/J.txt", f"{Data.SORTED_PATH}/Alphabetical/J.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/K.txt", f"{Data.SORTED_PATH}/Alphabetical/K.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/L.txt", f"{Data.SORTED_PATH}/Alphabetical/L.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/M.txt", f"{Data.SORTED_PATH}/Alphabetical/M.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/N.txt", f"{Data.SORTED_PATH}/Alphabetical/N.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/O.txt", f"{Data.SORTED_PATH}/Alphabetical/O.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/P.txt", f"{Data.SORTED_PATH}/Alphabetical/P.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Q.txt", f"{Data.SORTED_PATH}/Alphabetical/Q.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/R.txt", f"{Data.SORTED_PATH}/Alphabetical/R.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/S.txt", f"{Data.SORTED_PATH}/Alphabetical/S.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/T.txt", f"{Data.SORTED_PATH}/Alphabetical/T.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/U.txt", f"{Data.SORTED_PATH}/Alphabetical/U.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/V.txt", f"{Data.SORTED_PATH}/Alphabetical/V.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/W.txt", f"{Data.SORTED_PATH}/Alphabetical/W.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/X.txt", f"{Data.SORTED_PATH}/Alphabetical/X.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Y.txt", f"{Data.SORTED_PATH}/Alphabetical/Y.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
    (f"{Data.SORTED_PATH}/Alphabetical/Z.txt", f"{Data.SORTED_PATH}/Alphabetical/Z.{COMMON_TXT}", DEFAULT_MAX_PHRASES, DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH),
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

def get_common_phrases(input_file: str, output_file: str, max_phrases: int = 1000, min_length: int = 3, max_length: int = float('inf')) -> Optional[Counter]:
    # Validate parameters
    if max_phrases <= 0:
        logging.error("Parameter 'max_phrases' must be greater than 0.")
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

        # Split content into phrases using regex to handle punctuation and whitespace
        phrases = re.findall(r'\b\w+\b', content.lower())  # Example: words only, case insensitive

        # Filter phrases based on min and max length
        filtered_phrases = [phrase for phrase in phrases if min_length <= len(phrase) <= max_length]
        logging.info(f"Total phrases found: {len(phrases)}, filtered phrases: {len(filtered_phrases)}")

        # Count occurrences of each phrase
        phrase_counts = Counter(filtered_phrases)

        # Remove any phrases that are in the exclusions set
        for phrase in list(phrase_counts.keys()):
            if phrase in exclusions:
                del phrase_counts[phrase]

        logging.info(f"Excluded phrases: {len(phrase_counts)}")

        # Get the most common phrases
        common_phrases = phrase_counts.most_common(max_phrases)

        with open(output_file, 'w', encoding='utf-8') as file:
            for phrase, count in common_phrases:
                file.write(f"{count}: {phrase}\n")

        return phrase_counts  # Return the phrase counts as a Counter

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
    parser = argparse.ArgumentParser(description='Read links from a file and download their content to a specified output file')
    parser.add_argument('--i', '--input_file', type=str, default=DEFAULT_INPUT_FILE, help='Input link file (default: sourceLinks.txt)')
    parser.add_argument('--max_phrases', type=int, default=DEFAULT_MAX_PHRASES, help='Number of common phrases to retrieve (default: 1000)')
    parser.add_argument('--min_length', type=int, default=DEFAULT_MIN_LENGTH, help='Minimum length of phrases (default: 3)')
    parser.add_argument('--max_length', type=int, default=DEFAULT_MAX_LENGTH, help='Maximum length of phrases (default: 64)')
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
    # Check if no arguments were passed (i.e., defaults are used)
    if (args.i == DEFAULT_INPUT_FILE and
        args.max_phrases == DEFAULT_MAX_PHRASES and
        args.min_length == DEFAULT_MIN_LENGTH and
        args.max_length == DEFAULT_MAX_LENGTH):

        # Process each task in TASKS
        for input_file, output_file, max_phrases, min_length, max_length in TASKS:
            phrase_counts = get_common_phrases(input_file, output_file, max_phrases, min_length, max_length)
            if phrase_counts is not None:
                logging.info(f"Processed {len(phrase_counts)} common phrases from {input_file} ")
                logging.info(f"Added maximum of {max_phrases} common phrases to {output_file}")
                print()
    else:
        # Call the routine with the provided arguments
        phrase_counts = get_common_phrases(args.i, args.max_phrases, args.min_length, args.max_length)
        if phrase_counts is not None:
            logging.info(f"Processed {len(phrase_counts)} common phrases from {args.i} ")
            logging.info(f"Added maximum of {args.max_phrases} common phrases to common_phrases.txt")
            print()

if __name__ == "__main__":
    main()
