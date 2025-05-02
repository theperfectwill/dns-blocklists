# ---------------------------------
# Script Name: Code/Scripts/GetCommonPhrases.py
# Version: 1.0.0.0
# Description: This script reads text files, counts the occurrences of phrases,
#              and writes the most common phrases to output files.
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/GetCommonPhrases.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from collections import Counter
import logging
import os
import re
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

extracts_txt = "extracts.txt"
common_txt = "common.txt"

tasks = [
    (f"{_Vars.SORTED_PATH}/DomainParents/{extracts_txt}", f"{_Vars.SORTED_PATH}/DomainParents/{common_txt}", 1000),
    (f"{_Vars.SORTED_PATH}/DomainChildren/{extracts_txt}", f"{_Vars.SORTED_PATH}/DomainChildren/{common_txt}", 1000),
    (f"{_Vars.SORTED_PATH}/Conjoined/{extracts_txt}", f"{_Vars.SORTED_PATH}/Conjoined/{common_txt}", 1000),
    (f"{_Vars.SORTED_PATH}/OnlyLetters/{extracts_txt}", f"{_Vars.SORTED_PATH}/OnlyLetters/{common_txt}", 1000),
    (f"{_Vars.SORTED_PATH}/OnlyNumbers/{extracts_txt}", f"{_Vars.SORTED_PATH}/OnlyNumbers/{common_txt}", 50),
    (f"{_Vars.SORTED_PATH}/WildCards/{extracts_txt}", f"{_Vars.SORTED_PATH}/WildCards/{common_txt}", 1000),
]

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def get_common_phrases(input_file, output_file, num_common, phrase_counts=0):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split content into phrases using regex to handle punctuation
        phrases = re.findall(r'\b\w+\b', content.lower())  # Example: words only, case insensitive
        phrase_counts = Counter(phrases)
        common_phrases = phrase_counts.most_common(num_common)

        with open(output_file, 'w', encoding='utf-8') as file:
            for phrase, count in common_phrases:
                file.write(f"{count}: {phrase}\n")

        return phrase_counts  # Return the phrase counts

    except FileNotFoundError:
        logging.error(f"The file {input_file} was not found.")
    except IOError as e:
        logging.error(f"An IOError occurred: {e}")

    return None  # Return None if an error occurs

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    for input_file, output_file, num_common in tasks:
        phrase_counts = get_common_phrases(input_file, output_file, num_common)
        if phrase_counts is not None:
            logging.info(f"Processed {len(phrase_counts)} common phrases from {input_file} ")
            logging.info(f"Added maximum of {num_common} common phrases to {output_file}")
            print()

if __name__ == "__main__":
    main()
