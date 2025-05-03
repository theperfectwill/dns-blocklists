# ---------------------------------
# Script Name: CombinePatternRules.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/CombinePatternRules.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
import logging
import os
import re
import sys

# Helpers

# Custom
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Scripts'))
import _Vars

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**_Vars.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

strings_txt = f"{_Vars.RULES_PATH}/strings.txt"
regex_txt = f"{_Vars.RULES_PATH}/regex.txt"
combined_txt = f"{_Vars.RULES_PATH}/combined.txt"

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def read_filtered_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return [
                line.strip() for line in file
                if line.strip() and not line.startswith("!")
            ]
    except FileNotFoundError:
        logging.info(f"Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        logging.info(f"An error occurred while reading {file_path}: {e}")
        return []

def filter_special_characters(patterns):
    return [
        re.sub(r'[^a-zA-Z0-9\s-]', '', pattern)
        for pattern in patterns
    ]

def write_combined_patterns(strings_file, regex_file, output_file):
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

    try:
        with open(output_file, 'w') as file:
            file.write('\n'.join(combined_results) + '\n')
        logging.info(f"Combined optimized patterns written to {output_file}.")
    except Exception as e:
        logging.info(f"An error occurred while writing to {output_file}: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    write_combined_patterns(strings_txt, regex_txt, combined_txt)

if __name__ == "__main__":
    main()
