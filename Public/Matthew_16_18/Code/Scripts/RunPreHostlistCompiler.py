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
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our constants
# ---------------------------------

BLOCKLIST_JSON = Path(Data.SOURCES_PATH) / "blocklist.json"
BLOCKLIST_TXT = Path(Data.SOURCES_PATH) / "blocklist.txt"
WHITELIST_JSON = Path(Data.SOURCES_PATH) / "whitelist.json"
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
        process_hostlist(BLOCKLIST_JSON, BLOCKLIST_TXT)
        print()
        logging.info(f"Compiled {BLOCKLIST_JSON} to {BLOCKLIST_TXT}")
        print()

        # Process our whitelist
        process_hostlist(WHITELIST_JSON, WHITELIST_TXT)
        print()
        logging.info(f"Compiled {WHITELIST_JSON} to {WHITELIST_TXT}")
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
    setup_logging()
    run_pre_hostlist_compiler()

if __name__ == "__main__":
    main()
