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
        last_modified = time.ctime(last_modified_timestamp)  # Convert to a readable format

        # Get the line count of the file minus the file_comments count (currently 12)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file_count = max(0, len(lines) - 12)  # Ensure file_count is not negative

        # Delete lines starting with "!" except "! Source:"
        lines = [line.strip() for line in lines if not line.startswith("!") or line.startswith("! Source:")]

        # Insert the file_comments at the top of the file if it doesn't already exist
        file_comments = (
            f"! Title: RegexDNSF {_Vars.FOLDER_NAME}\n"
            f"! Description: My description here....\n"
            f"! Homepage: https://github.com/theperfectwill/dns-regex-filters\n"
            f"! Version: 2025.0502.0219.22\n"
            f"! License: https://github.com/theperfectwill/dns-regex-filters/blob/main/LICENSE\n"
            f"! Issues: https://github.com/theperfectwill/dns-regex-filters/issues\n"
            f"! Last modified: {last_modified}\n"
            f"! Expires: 1 day\n"
            f"! Number of entries: {file_count}\n"
            f"! Syntax: AdBlock\n"
            f"! Author: ThePerfectWill\n"
            f"! Compiled by @adguard/hostlist-compiler\n"
            f"! \n"
        )

        if file_comments.strip() not in lines:
            lines.insert(0, file_comments)  # Insert file_comments at the beginning of the list

        # Write the filtered lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(line + '\n' for line in lines)  # Write the combined list back to the file

        print(f"File '{file_path}' processed successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError as e:
        print(f"IO error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing the file: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    run_final_hostlist_compiler()
    reformat_final_file(final_txt)

if __name__ == "__main__":
    main()
