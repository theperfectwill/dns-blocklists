# ---------------------------------
# Script Name: SortByRegexPatterns.py
# Version: 1.0.1.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/SortByRegexPatterns.py
# --i _Input_File_ --o _Output_Path_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from collections import defaultdict
from pathlib import Path
from typing import List, Dict
import argparse
import logging
import re
import sys

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

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

def get_regex_patterns(lines: List[str]) -> Dict[str, List[str]]:
    patterns = {
        "DomainParents": re.compile(r"\b([|]?)([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})([|^]?)(?=\s|$)"),
        "DomainChildren": re.compile(r"^(?![a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"),
        "OnlyLetters": re.compile(r"^[A-Za-z]+$"),
        "Conjoined": re.compile(r"^([a-zA-Z]+([ _-][a-zA-Z]+){0,99})?$"),
        "WildCards": re.compile(r"^.*\*.*$"),
        "OnlyNumbers": re.compile(r"^[0-9]+$")
    }

    extracted_data = defaultdict(list)

    for line in lines:
        for key, pattern in patterns.items():
            match = pattern.search(line)
            if match:
                extracted_data[key].append(match.group())

    return extracted_data

def filter_and_sort_data(data: List[str]) -> List[str]:
    # Filter data to include only items with 4 or more characters, remove duplicates, and sort.
    return sorted(set(item for item in data if len(item) >= 4))

def save_to_file(file_path: Path, data: List[str]) -> None:
    with file_path.open("w") as file:
        file.write("\n".join(data))

def save_matching_regex_patterns(extracted_data: Dict[str, List[str]], output_dir: str) -> None:
    for key, data in extracted_data.items():
        dir_path = Path(output_dir) / key
        file_path = dir_path / "extracts.txt"

        # Create directory if it doesn't exist
        dir_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {dir_path}")

        # Filter, sort, and remove duplicates
        filtered_data = filter_and_sort_data(data)

        # Log the number of extracted patterns
        num_original_patterns = len(data)
        num_filtered_patterns = len(filtered_data)
        logging.info(f"Extracted {num_original_patterns} patterns, filtered to {num_filtered_patterns} matching regex patterns to {file_path}")

        save_to_file(file_path, filtered_data)

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Sort lines by regex patterns.")
    parser.add_argument('--i', '--input_file', type=str, default=f"{Data.SOURCES_PATH}/blocklist.txt", help='Path to the blocklist file (default: Data.SOURCES_PATH/blocklist.txt)')
    parser.add_argument('--o', '--output_file', type=str, default=str(Path(Data.SORTED_PATH)), help='Directory to save matching regex patterns (default: Data.SORTED_PATH)')
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

    # Read lines from the i
    with open(args.i, "r") as file:
        lines = file.readlines()

    extracted_data = get_regex_patterns(lines)
    save_matching_regex_patterns(extracted_data, args.o)

    # Log total patterns extracted
    total_patterns = sum(len(data) for data in extracted_data.values())
    logging.info(f"Total patterns extracted: {total_patterns}")
    # logging.info(f"Total patterns written: {num_filtered_patterns}")

# Call the main function
if __name__ == "__main__":
    main()
