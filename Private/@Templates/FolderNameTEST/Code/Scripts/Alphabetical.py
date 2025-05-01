# ---------------------------------
# Script Name: Alphabetical.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/Alphabetical.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

# Core
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

blocklist_txt = "blocklist.txt"
output_dir = os.path.join(_Vars.SORTED_PATH, "Alphabetical")

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def sort_blocklist():
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Open the input file
        with open(os.path.join(_Vars.SOURCES_PATH, blocklist_txt), "r") as f:
            # Read the contents of the file
            lines = f.readlines()

        # Create a dictionary to store the entries by their first letter
        entries_by_letter = {chr(i + 65): [] for i in range(26)}

        # Iterate through the lines and sort them by their first letter
        for line in lines:
            first_letter = line.strip()[0].upper()
            if first_letter.isalpha():
                entries_by_letter[first_letter].append(line.strip())

        # Write the entries to their respective files
        for letter, entries in entries_by_letter.items():
            if entries:
                with open(os.path.join(output_dir, f"{letter}.txt"), "w") as f:
                    f.write("\n".join(sorted(entries)))
                    logging.info(f"Compiled all entries starting with letter {letter} to {output_dir}/{letter}.txt")

    except FileNotFoundError:
        logging.info(f"Error: {_Vars.SOURCES_PATH}/{blocklist_txt} not found.")
    except PermissionError:
        logging.info(f"Error: Unable to access {_Vars.SOURCES_PATH}/{blocklist_txt} or {output_dir}.")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    sort_blocklist()

if __name__ == "__main__":
    main()
