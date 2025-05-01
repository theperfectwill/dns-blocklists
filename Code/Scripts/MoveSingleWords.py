# ---------------------------------
# Script Name: fileName.sh
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3 $thisPythonFile $fileToCheck $numPhraseLength $numTopPhraseAmount $resultOutputFile
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

import argparse

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def move_single_word_lines(file_input, file_output):
    try:
        # Open the input file for reading
        with open(file_input, 'r') as infile:
            # Read all lines from the input file
            lines = infile.readlines()
        
        # Prepare lists to hold single-word lines and remaining lines
        single_word_lines = []
        remaining_lines = []

        # Check each line for single-word content
        for line in lines:
            # Strip whitespace and check if the line contains only one word
            if len(line.strip().split()) == 1:
                single_word_lines.append(line.strip())
            else:
                remaining_lines.append(line)

        # Open the output file for writing
        with open(file_output, 'a') as outfile:
            # Write the single-word lines to the output file
            for word_line in single_word_lines:
                outfile.write(word_line + '\n')

        # Write the remaining lines back to the input file
        with open(file_input, 'w') as infile:
            infile.writelines(remaining_lines)

        print(f"Moved {len(single_word_lines)} single-word lines to {file_output} and updated {file_input}.")

    except FileNotFoundError:
        print(f"Error: The file '{file_input}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Move single-word lines from input file to output file.')
    parser.add_argument('file_input', type=str, help='The input file to scan for single-word lines.')
    parser.add_argument('file_output', type=str, help='The output file to write single-word lines to.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    move_single_word_lines(args.file_input, args.file_output)

if __name__ == "__main__":
    main()
