# ---------------------------------
# Script Name: Code/Scripts/GetCommonPhrases.py
# Version: 1.0.0.0
# Description: This script reads text files, counts the occurrences of phrases, and writes the most common phrases to output files.
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
exclusions_txt = "exclusions.txt"

tasks = [
    # Special
    (f"{_Vars.SORTED_PATH}/DomainParents/{extracts_txt}", f"{_Vars.SORTED_PATH}/DomainParents/{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/DomainChildren/{extracts_txt}", f"{_Vars.SORTED_PATH}/DomainChildren/{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Conjoined/{extracts_txt}", f"{_Vars.SORTED_PATH}/Conjoined/{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/OnlyLetters/{extracts_txt}", f"{_Vars.SORTED_PATH}/OnlyLetters/{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/OnlyNumbers/{extracts_txt}", f"{_Vars.SORTED_PATH}/OnlyNumbers/{common_txt}", 50, 5, 64),
    (f"{_Vars.SORTED_PATH}/WildCards/{extracts_txt}", f"{_Vars.SORTED_PATH}/WildCards/{common_txt}", 1000, 3, 64),
    # Alphabetical
    (f"{_Vars.SORTED_PATH}/Alphabetical/A.txt", f"{_Vars.SORTED_PATH}/Alphabetical/A.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/B.txt", f"{_Vars.SORTED_PATH}/Alphabetical/B.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/C.txt", f"{_Vars.SORTED_PATH}/Alphabetical/C.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/D.txt", f"{_Vars.SORTED_PATH}/Alphabetical/D.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/E.txt", f"{_Vars.SORTED_PATH}/Alphabetical/E.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/F.txt", f"{_Vars.SORTED_PATH}/Alphabetical/F.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/G.txt", f"{_Vars.SORTED_PATH}/Alphabetical/G.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/H.txt", f"{_Vars.SORTED_PATH}/Alphabetical/H.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/I.txt", f"{_Vars.SORTED_PATH}/Alphabetical/I.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/J.txt", f"{_Vars.SORTED_PATH}/Alphabetical/J.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/K.txt", f"{_Vars.SORTED_PATH}/Alphabetical/K.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/L.txt", f"{_Vars.SORTED_PATH}/Alphabetical/L.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/M.txt", f"{_Vars.SORTED_PATH}/Alphabetical/M.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/N.txt", f"{_Vars.SORTED_PATH}/Alphabetical/N.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/O.txt", f"{_Vars.SORTED_PATH}/Alphabetical/O.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/P.txt", f"{_Vars.SORTED_PATH}/Alphabetical/P.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/Q.txt", f"{_Vars.SORTED_PATH}/Alphabetical/Q.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/R.txt", f"{_Vars.SORTED_PATH}/Alphabetical/R.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/S.txt", f"{_Vars.SORTED_PATH}/Alphabetical/S.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/T.txt", f"{_Vars.SORTED_PATH}/Alphabetical/T.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/U.txt", f"{_Vars.SORTED_PATH}/Alphabetical/U.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/V.txt", f"{_Vars.SORTED_PATH}/Alphabetical/V.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/W.txt", f"{_Vars.SORTED_PATH}/Alphabetical/W.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/X.txt", f"{_Vars.SORTED_PATH}/Alphabetical/X.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/Y.txt", f"{_Vars.SORTED_PATH}/Alphabetical/Y.{common_txt}", 1000, 3, 64),
    (f"{_Vars.SORTED_PATH}/Alphabetical/Z.txt", f"{_Vars.SORTED_PATH}/Alphabetical/Z.{common_txt}", 1000, 3, 64),
]

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def get_common_phrases(input_file, output_file, num_common, min_length=3, max_length=float('inf'), phrase_counts=0):
    try:
        # Read exclusions from the specified file
        exclusions = set()
        with open(f"{_Vars.RULES_PATH}/{exclusions_txt}", 'r', encoding='utf-8') as exclusions_file:
            for line in exclusions_file:
                line = line.strip()
                if line and not line.startswith("!"):  # Skip empty lines and lines starting with "!"
                    exclusions.add(line)

        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split content into phrases using regex to handle punctuation
        phrases = re.findall(r'\b\w+\b', content.lower())  # Example: words only, case insensitive

        # Filter phrases based on min and max length
        filtered_phrases = [phrase for phrase in phrases if min_length <= len(phrase) <= max_length]

        # Count occurrences of each phrase
        phrase_counts = Counter(filtered_phrases)

        # Remove any phrases that are in the exclusions set
        for exclusion in exclusions:
            if exclusion in phrase_counts:
                del phrase_counts[exclusion]

        # Get the most common phrases
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
    for input_file, output_file, num_common, min_length, max_length in tasks:
        phrase_counts = get_common_phrases(input_file, output_file, num_common, min_length, max_length)
        if phrase_counts is not None:
            logging.info(f"Processed {len(phrase_counts)} common phrases from {input_file} ")
            logging.info(f"Added maximum of {num_common} common phrases to {output_file}")
            print()

if __name__ == "__main__":
    main()
