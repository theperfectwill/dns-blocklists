# ---------------------------------
# Script Name: ExtractRegexPatterns.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/ExtractRegexPatterns.py
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

def extract_patterns(lines):
    patterns = {
        "DomainParents": r"\b([|]?)([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})([|^]?)(?=\s|$)",
        "DomainChildren": r"^(?![a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
        "OnlyLetters": r"^[A-Za-z]+$",
        "Conjoined": r"^([a-zA-Z]+([ _-][a-zA-Z]+){0,99998})?$",
        "WildCards": r"^.*\*.*$",
        "OnlyNumbers": r"^[0-9]+$"
    }

    extracted_data = {key: [] for key in patterns.keys()}

    for line in lines:
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                extracted_data[key].append(match.group())

    return extracted_data

def save_extracted_data(extracted_data):
    for key, data in extracted_data.items():
        logging.info(f"Extracted matching regex patterns to {_Vars.SORTED_PATH}/{key}/extracts.txt")
        with open(f"{_Vars.SORTED_PATH}/{key}/extracts.txt", "w") as file:
            file.write("\n".join(data))

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    try:
        with open(f"{_Vars.SOURCES_PATH}/blocklist.txt", "r") as file:
            lines = file.readlines()

        extracted_data = extract_patterns(lines)
        save_extracted_data(extracted_data)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
