# ---------------------------------
# Script Name: fileNameHere.sh
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

import Vars
import subprocess
import os

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

final_dir = "Final"
final_json = f"{final_dir}/regexDNSF.json"
final_txt = f"{final_dir}/regexDNSF.txt"

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def process_hostlist(input_file, output_file):
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
        # Run hostlist-compiler for final regexDNSF
        process_hostlist(final_json, final_txt)

    except subprocess.CalledProcessError as e:
        print(f"Error running hostlist-compiler command: {e}")
    except FileNotFoundError:
        print("Error: Final directory or files not found.")
    except IOError:
        print("Error: Unable to read or write to file.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

def process_file(file_path):
    try:
        # Read the existing lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Delete lines starting with "!" from the blocklist
        lines = [line.strip() for line in lines if not line.startswith(("!"))]

        # Insert the file_comments at the top of the file if it doesn't already exist
        file_comments = f"! Title: RegexDNSF {Vars.FolderName}\n"
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
    process_file(final_txt)

if __name__ == "__main__":
    main()
