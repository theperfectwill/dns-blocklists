# ---------------------------------
# Script Name: Alphabetical.py
# Version: 1.0.0.0
# Description: The function sort_input_alphabetically organizes entries from a specified blocklist file into separate alphabetically sorted text files based on their starting letters.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/Alphabetical.py
# --i _Input_File_ --o _Output_Path_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

# Core
from collections import defaultdict
from pathlib import Path
import argparse
import logging
import re
import sys

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our constants
# ---------------------------------

BLOCKLIST_TXT = Path(Data.SOURCES_PATH) / "blocklist.txt"
DEFAULT_OUTPUT_DIR = Path(Data.SORTED_PATH)

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

def setup_logging(logging_level: str) -> None:
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

def sort_input_alphabetically(input_file: str, output_dir: Path) -> None:
    output_dir = output_dir / "Alphabetical"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(input_file, "r") as f:
            # Strip lines of leading and trailing special characters
            lines = [re.sub(r'^[^\w\s]+|[^\w\s]+$', '', line.strip()) for line in f if line.strip()]

        if not lines:
            logging.warning(f"The input file '{input_file}' is empty.")
            return

        entries_by_letter = defaultdict(list)

        for line in lines:
            first_letter = line[0].upper() if line else ''
            if first_letter.isalpha():
                entries_by_letter[first_letter].append(line)

        for letter, entries in entries_by_letter.items():
            with open(output_dir / f"{letter}.txt", "w") as f:
                f.write("\n".join(sorted(entries)))
                logging.info(f"Compiled {len(entries)} entries starting with letter '{letter}' to '{output_dir}/{letter}.txt'")

    except FileNotFoundError:
        logging.error(f"Error: {input_file} not found.")
    except PermissionError:
        logging.error(f"Error: Unable to access {input_file} or {output_dir}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Sort entries from a blocklist into alphabetical files.')
    parser.add_argument('--i', '--input_file', type=str, default=BLOCKLIST_TXT, help='Input blocklist file (default: blocklist.txt)')
    parser.add_argument('--o', '--output_file', type=str, default=str(DEFAULT_OUTPUT_DIR), help='Output directory for sorted files (default: Alphabetical in SORTED_PATH)')
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
    validate_output_directory(args.o)

    # Now call any routines
    sort_input_alphabetically(args.i, Path(args.o))

if __name__ == "__main__":
    main()
