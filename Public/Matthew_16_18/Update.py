# ---------------------------------
# Script Name: Update.py
# Version: 1.0.0.0
# Description: Calls all our other scripts in updating this folder, applying any new changes.
#  Those changes can be 3rdParty blocklist updates, new wildcard/regex replacements,
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/Update.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core & Helpers
from pathlib import Path
import logging
import subprocess
import sys
import time

# Helpers

# Custom Modules
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

SCRIPTS = [
    # Update these strings or search and replace them
    #  ThisFolderName
    #  1.0.0.0
    # f"{Data.UpdateStrings_py}",
    # f"{Data.DownloadRepoLinks_py}",
    # f"{Data.RunPreHostlistCompiler_py}",
    # f"{Data.FormatLists_py}",
    # f"{Data.Alphabetical_py}",
    # f"{Data.SortByRegexPatterns_py}",
    # f"{Data.GetCommonPhrases_py}",
    f"{Data.CombinePatternRules_py}",
    f"{Data.RunFinalHostlistCompiler_py}"
]

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

def run_script(script: str) -> bool:
    script_path = Path(script)
    if not script_path.is_file():
        logging.error(f"Script not found: {script}")
        return False

    start_time = time.time()
    try:
        result = subprocess.run([Data.PYTHON_VER, script], check=True, text=True, capture_output=True)
        execution_time = time.time() - start_time
        logging.info(f"{script} - Successfully executed in {execution_time:.2f} seconds.")
        logging.debug(f"{script} - Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"{script} - Error executing: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"{script} - An unexpected error occurred: {e}")
        return False

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main() -> None:
    setup_logging()

    success_count = 0
    failure_count = 0

    for script in SCRIPTS:
        if run_script(script):
            success_count += 1
        else:
            failure_count += 1

    # Summary of execution
    logging.info(f"Execution Summary: {success_count} scripts executed successfully, {failure_count} scripts failed.")

if __name__ == "__main__":
    main()
