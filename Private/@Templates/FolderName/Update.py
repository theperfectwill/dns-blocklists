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
import logging
import os
import subprocess
import sys
import time

# Custom Modules
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Scripts'))
import _Vars

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**_Vars.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

scripts = [
    # f"{_Vars.SCRIPTS_PATH}/UpdateStrings.py",
    f"{_Vars.SCRIPTS_PATH}/DownloadRepoLinks.py",
    f"{_Vars.SCRIPTS_PATH}/RunPreHostlistCompiler.py",
    f"{_Vars.SCRIPTS_PATH}/FormatLists.py",
    f"{_Vars.SCRIPTS_PATH}/Alphabetical.py",
    f"{_Vars.SCRIPTS_PATH}/SortByRegexPatterns.py",
    f"{_Vars.SCRIPTS_PATH}/GetCommonPhrases.py",
    f"{_Vars.SCRIPTS_PATH}/CombinePatternRules.py",
    f"{_Vars.SCRIPTS_PATH}/RunFinalHostlistCompiler.py"
]

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def run_script(script):
    try:
        # Check if the script exists
        if not os.path.isfile(script):
            raise FileNotFoundError(f"Script not found: {script}")

        # Start time measurement
        start_time = time.time()

        # Execute the script
        result = subprocess.run(['python3', script], check=True, text=True, capture_output=True)

        # End time measurement
        end_time = time.time()

        # Calculate execution time
        execution_time = end_time - start_time

        # Print our success, output and task time
        logging.info(f"{script} - Successfully executed.")
        # logging.info("Output:", result.stdout)
        logging.info(f"{script} - Execution time: {execution_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        logging.info(f"{script} - Error executing: {e.stderr}")
    except FileNotFoundError as e:
        logging.info(e)
    except Exception as e:
        logging.info(f"{script} - An unexpected error occurred while executing: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    for script in scripts:
        run_script(script)
        print()

if __name__ == "__main__":
    main()
