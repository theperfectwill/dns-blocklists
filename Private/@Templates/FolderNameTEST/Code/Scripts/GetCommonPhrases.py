# ---------------------------------
# Script Name: GetCommonPhrases.py
# Version: 1.0.0.0
# Description: This script reads text files, counts the occurrences of phrases,
#              and writes the most common phrases to output files.
# Author: ThePerfectWill
# Usage: python3 GetCommonPhrases.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from collections import Counter
import logging
import os
import subprocess
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

input_file = os.path.join(_Vars.SOURCES_PATH, "blocklist.txt")

extracts = [
    (f"{_Vars.SORTED_PATH}/DomainParents/extracts.txt", f"{_Vars.SORTED_PATH}/DomainParents/common.txt", 1000),
    (f"{_Vars.SORTED_PATH}/DomainChildren/extracts.txt", f"{_Vars.SORTED_PATH}/DomainChildren/common.txt", 1000),
    (f"{_Vars.SORTED_PATH}/Conjoined/extracts.txt", f"{_Vars.SORTED_PATH}/Conjoined/common.txt", 1000),
    (f"{_Vars.SORTED_PATH}/OnlyLetters/extracts.txt", f"{_Vars.SORTED_PATH}/OnlyLetters/common.txt", 1000),
    (f"{_Vars.SORTED_PATH}/OnlyNumbers/extracts.txt", f"{_Vars.SORTED_PATH}/OnlyNumbers/common.txt", 50),
    (f"{_Vars.SORTED_PATH}/WildCards/extracts.txt", f"{_Vars.SORTED_PATH}/WildCards/common.txt", 1000),
]

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def ensure_output_directory(output_file):
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

def get_common_phrases(input_file, output_file, num_common):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split content into phrases (considering punctuation and case)
        phrases = content.split()
        phrase_counts = Counter(phrases)
        common_phrases = phrase_counts.most_common(num_common)

        with open(output_file, 'w', encoding='utf-8') as file:
            for phrase, count in common_phrases:
                file.write(f"{phrase}: {count}\n")

    except FileNotFoundError:
        logging.error(f"The file {input_file} was not found.")
    except IOError as e:
        logging.error(f"An IOError occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    for input_file, output_file, num_common in extracts:
        ensure_output_directory(output_file)
        get_common_phrases(input_file, output_file, num_common)

if __name__ == "__main__":
    main()
