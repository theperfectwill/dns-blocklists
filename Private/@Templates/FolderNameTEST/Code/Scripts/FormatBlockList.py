# ---------------------------------
# Script Name: FormatBlocklist.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 FormatBlocklist.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
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

blocklist_txt = os.path.join(_Vars.SOURCES_PATH, "blocklist.txt")
strings_txt = os.path.join(_Vars.RULES_PATH, "strings.txt")
regex_txt = os.path.join(_Vars.RULES_PATH, "regex.txt")

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def format_blocklist():
    try:
        # Read the blocklist
        with open(blocklist_txt, "r") as file:
            lines = file.readlines()

        # Alphabetically sort the blocklist
        lines.sort()
        logging.info(f"Alphabetically sorted {blocklist_txt}")

        # Delete lines starting with "!" or "#" from the blocklist
        lines = [line.strip() for line in lines if not line.startswith(("!", "#"))]
        logging.info(f"Deleted lines starting with ! or # from {blocklist_txt}")

        # Delete lines containing all digits and only one TLD from the blocklist
        lines = [line for line in lines if not (line.isdigit() and line.count(".") == 1)]
        logging.info(f"Deleted lines containing all digits and only one TLD from {blocklist_txt}")

        # Delete the "^" character and everything after it from lines in the blocklist
        lines = [re.sub(r"\^.*", "", line) for line in lines]
        logging.info(f"Deleted ^ characters and everything after them from {blocklist_txt}")

        # Delete the "$" character and everything after it from lines in the blocklist
        lines = [re.sub(r"\$.*", "", line) for line in lines]
        logging.info(f"Deleted $ characters and everything after them from {blocklist_txt}")

        # Remove all '|' characters from the blocklist
        lines = [line.replace('|', '') for line in lines]
        logging.info(f"Removed all | characters from {blocklist_txt}")

        # @ToCheck->Remove because we do this removal+replacement of (regex|strings) through hostlist-compiler

        # Delete lines containing any string from strings.txt from the blocklist
        # try:
        #     with open(strings_txt, "r") as file:
        #         strings = [line.strip() for line in file.readlines()]
        # except FileNotFoundError:
        #     print(f"File not found: {strings_txt}")
        #     return

        # lines = [line for line in lines if not any(s in line for s in strings)]

        # Delete lines matching any regex pattern in regex.txt from the blocklist
        # try:
        #     with open(regex_txt, "r") as file:
        #         regexes = [line.strip().strip('/') for line in file.readlines()]
        # except FileNotFoundError:
        #     print(f"File not found: {regex_txt}")
        #     return

        # lines = [line for line in lines if not any(re.match(r, line) for r in regexes)]

        # Write the modified lines back to the blocklist
        with open(blocklist_txt, "w") as file:
            if lines:  # Only write if there are lines to write
                file.writelines("\n".join(lines) + "\n")
            else:
                print("No valid lines to write to the blocklist.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    format_blocklist()

if __name__ == "__main__":
    main()
