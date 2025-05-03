# ---------------------------------
# Script Name: RunFinalHostlistCompiler.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/RunFinalHostlistCompiler.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from datetime import datetime
import logging
import os
import subprocess
import sys
import time

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

final_json = os.path.join(_Vars.FINAL_PATH, "regexDNSF.json")
final_txt = os.path.join(_Vars.FINAL_PATH, "regexDNSF.txt")
blocklist_txt = os.path.join(_Vars.SOURCES_PATH, "blocklist.txt")

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

def run_final_hostlist_compiler():
    try:
        # Process our finalist
        process_hostlist(final_json, final_txt)
        print()
        logging.info(f"Compiled {final_json} to {final_txt}")
        print()

    except subprocess.CalledProcessError as e:
        logging.info(f"Error running hostlist-compiler command: {e}")
    except FileNotFoundError:
        logging.info("Error: Sources directory or files not found.")
    except IOError:
        logging.info("Error: Unable to read or write to file.")
    except Exception as e:
        logging.info(f"Unexpected error occurred: {e}")

def reformat_final_file(file_path):
    try:
        # Get the last modified time of the file
        last_modified_timestamp = os.path.getmtime(file_path)
        last_modified = datetime.fromtimestamp(last_modified_timestamp).strftime('%A, %B %d, %Y %I:%M %p')

        # Get the line count of Sources/sourceDownloads.txt
        with open(blocklist_txt, 'r') as source_file:
            original_rule_count = len(source_file.readlines())

        # Get the line count of the file minus the file_comments count (currently 12)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            current_rule_count = max(0, len(lines) - 15)  # Ensure current_rule_count is not negative

        # Calculate reduced_rule_count
        reduced_rule_count = original_rule_count - current_rule_count

        # Delete lines starting with "!" except "! Source:"
        lines = [line.strip() for line in lines if not line.startswith("!") or line.startswith("! Source:")]
        logging.info(f"{file_path} - Deleted all lines starting with \"!\" except \"! Source:\"")

        # Insert the file_comments at the top of the file if it doesn't already exist
        # @Note->when adding a new comment change current_rule_count ↑ to reflect the correct calculation
        file_comments = (
            f"{_Vars.TITLE_COMMENT}\n"
            f"{_Vars.DESC_COMMENT}\n"
            f"{_Vars.HOMEPAGE_COMMENT}\n"
            f"{_Vars.VERSION_COMMENT}\n"
            f"{_Vars.LICENSE_COMMENT}\n"
            f"{_Vars.ISSUES_COMMENT}\n"
            f"{_Vars.EXPIRES_COMMENT}\n"
            f"{_Vars.LAST_MOD_COMMENT}{last_modified}\n"
            f"{_Vars.CURRENT_RULE_COUNT_COMMENT}{current_rule_count}\n"
            f"{_Vars.ORIGINAL_RULE_COUNT_COMMENT}{original_rule_count}\n"
            f"{_Vars.RULE_REDUCED_COUNT_COMMENT}{reduced_rule_count}\n"
            f"{_Vars.RULE_REDUCTION_NOTES_COMMENT}\n"
            f"{_Vars.SYNTAX_COMMENT}\n"
            f"{_Vars.AUTHOR_COMMENT}\n"
            f"{_Vars.COMPILED_COMMENT}"
        )

        if file_comments.strip() not in lines:
            lines.insert(0, file_comments)  # Insert file_comments at the beginning of the list
            logging.info(f"{file_path} - Added header file comments.")

        # Write the filtered lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(line + '\n' for line in lines)  # Write the combined list back to the file

        logging.info(f"{file_path} - Processed successfully.")
    except FileNotFoundError:
        logging.info(f"Error: The file '{file_path}' or '{blocklist_txt}' was not found.")
    except IOError as e:
        logging.info(f"IO error occurred: {e}")
    except Exception as e:
        logging.info(f"An unexpected error occurred while processing the file: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    run_final_hostlist_compiler()
    reformat_final_file(final_txt)

if __name__ == "__main__":
    main()
