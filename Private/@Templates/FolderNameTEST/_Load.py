# ---------------------------------
# Script Name: _Load.py
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage: python3 _Load.py
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
    # f"{_Vars.SCRIPTS_PATH}/StringUpdates.py",
    f"{_Vars.SCRIPTS_PATH}/DownloadRepoLinks.py",
    f"{_Vars.SCRIPTS_PATH}/RunPreHostlistCompiler.py",
    f"{_Vars.SCRIPTS_PATH}/FormatBlockList.py",
    f"{_Vars.SCRIPTS_PATH}/Alphabetical.py",
    f"{_Vars.SCRIPTS_PATH}/ExtractRegexPatterns.py",
    f"{_Vars.SCRIPTS_PATH}/GetCommonPhrases.py",
    # f"{_Vars.SCRIPTS_PATH}/RunFinalHostlistCompiler.py"
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
        logging.info(f"Successfully executed: {script}")
        # logging.info("Output:", result.stdout)
        logging.info(f"Execution time: {execution_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        logging.info(f"Error executing {script}: {e.stderr}")
    except FileNotFoundError as e:
        logging.info(e)
    except Exception as e:
        logging.info(f"An unexpected error occurred while executing {script}: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    for script in scripts:
        run_script(script)
        # logging.info(f"Processed: {script}")
        print()

if __name__ == "__main__":
    main()
