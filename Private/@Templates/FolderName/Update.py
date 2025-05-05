# ---------------------------------
# Script Name: Update.py
# Version: 1.0.0.0
# Description: Calls all our other scripts in updating this folder, applying any new changes.
#  Those changes can be 3rdParty blocklist updates, new wildcard/regex replacements,
# Author: ThePerfectWill
# Usage: python3 Update.py
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

# Custom Modules
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts'))
import Data

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**Data.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

scripts = [
    # f"{UpdateStrings_py}",
    f"{DownloadRepoLinks_py}",
    f"{RunPreHostlistCompiler_py}",
    f"{FormatLists_py}",
    f"{Alphabetical_py}",
    f"{SortByRegexPatterns_py}",
    f"{GetCommonPhrases_py}",
    f"{CombinePatternRules_py}",
    f"{RunFinalHostlistCompiler_py}"
]

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
    success_count = 0
    failure_count = 0

    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            failure_count += 1

    # Summary of execution
    logging.info(f"Execution Summary: {success_count} scripts executed successfully, {failure_count} scripts failed.")

if __name__ == "__main__":
    main()
