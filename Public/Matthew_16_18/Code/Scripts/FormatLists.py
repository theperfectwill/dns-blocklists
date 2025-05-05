# ---------------------------------
# Script Name: FormatLists.py
# Version: 1.0.0.0
# Description: The function format_file formats/strips a blocklist to our liking
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/FormatLists.py
# --i _Input_File_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

# Core
from pathlib import Path
import argparse
import logging
import re
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

BLOCKLIST_TXT = Path(Data.SOURCES_PATH) / "blocklist.txt"
WHITELIST_TXT = Path(Data.SOURCES_PATH) / "whitelist.txt"

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

def format_file(file_input):
    try:
        # Read the blocklist
        with open(file_input, "r") as file:
            lines = file.readlines()

        # Alphabetically sort the blocklist
        lines.sort()
        logging.info(f"{file_input} - Alphabetically sorted")

        # Delete lines starting with "!" or "#" from the blocklist
        lines = [line.strip() for line in lines if not line.startswith(("!", "#"))]
        logging.info(f"{file_input} - Deleted lines starting with ! or #")

        # Delete lines containing all digits and only one TLD from the blocklist
        lines = [line for line in lines if not (line.isdigit() and line.count(".") == 1)]
        logging.info(f"{file_input} - Deleted lines containing all digits and only one TLD")

        # Delete lines that contain only one character
        lines = [line for line in lines if len(line) > 1]
        logging.info(f"{file_input} - Deleted lines containing only one character")

        # Delete the "^" character and everything after it from lines in the blocklist
        lines = [re.sub(r"\^.*", "", line) for line in lines]
        logging.info(f"{file_input} - Deleted ^ characters and everything after them")

        # Delete the "$" character and everything after it from lines in the blocklist
        lines = [re.sub(r"\$.*", "", line) for line in lines]
        logging.info(f"{file_input} - Deleted $ characters and everything after them")

        # Remove all '|' characters from the blocklist
        lines = [line.replace('|', '') for line in lines]
        logging.info(f"{file_input} - Removed all | characters")

        # Remove all '@' characters from the blocklist
        lines = [line.replace('@', '') for line in lines]
        logging.info(f"{file_input} - Removed all @ characters")

        # Write the modified lines back to the blocklist
        with open(file_input, "w") as file:
            if lines:  # Only write if there are lines to write
                file.writelines("\n".join(lines) + "\n")
            else:
                loggin.info("No valid lines to write to the blocklist.")

    except FileNotFoundError as e:
        loggin.info(f"File not found: {e.filename}")
    except Exception as e:
        loggin.info(f"An error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Read links from a file and download their content to a specified output file')
    parser.add_argument('--i', '--input_file', type=str, help='Input file path to format (default: none)')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    # Now call any routines
    if args.i:
        # Validate input file
        validate_input_file(args.i)
        format_file(args.i)
    else:
        # If no input is passed, process both BLOCKLIST_TXT and WHITELIST_TXT
        format_file(BLOCKLIST_TXT)
        format_file(WHITELIST_TXT)

if __name__ == "__main__":
    main()
