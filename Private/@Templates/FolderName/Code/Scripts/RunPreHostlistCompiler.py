# ---------------------------------
# Script Name: RunPreHostlistCompiler.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/RunPreHostlistCompiler.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from pathlib import Path
import logging
import os
import subprocess
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts'))
import Data

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**Data.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

blocklist_json = os.path.join(Data.SOURCES_PATH, "blocklist.json")
blocklist_txt = os.path.join(Data.SOURCES_PATH, "blocklist.txt")
whitelist_json = os.path.join(Data.SOURCES_PATH, "whitelist.json")
whitelist_txt = os.path.join(Data.SOURCES_PATH, "whitelist.txt")

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def process_hostlist(input_file, output_file):
    # Run our hostlist-compiler
    subprocess.run(["hostlist-compiler", "-c", input_file, "-o", output_file], check=True)

    # Remove lines that start with "!" and have no characters after it
    with open(output_file, "r") as file:
        lines = file.readlines()
    with open(output_file, "w") as file:
        for line in lines:
            if not (line.startswith("!") and len(line.strip()) == 1):
                file.write(line)

def run_pre_hostlist_compiler():
    try:
        # Process our blocklist
        process_hostlist(blocklist_json, blocklist_txt)
        print()
        logging.info(f"Compiled {blocklist_json} to {blocklist_txt}")
        print()
        
        # Process our whitelist
        process_hostlist(whitelist_json, whitelist_txt)
        print()
        logging.info(f"Compiled {whitelist_json} to {whitelist_txt}")
        print()

    except subprocess.CalledProcessError as e:
        logging.info(f"Error running hostlist-compiler command: {e}")
    except FileNotFoundError:
        logging.info("Error: Sources directory or files not found.")
    except IOError:
        logging.info("Error: Unable to read or write to file.")
    except Exception as e:
        logging.info(f"Unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    run_pre_hostlist_compiler()

if __name__ == "__main__":
    main()
