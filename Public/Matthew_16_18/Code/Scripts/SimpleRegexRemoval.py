# ---------------------------------
# Script Name: SimpleRegexRemoval.py
# Version: 1.0.0.0
# Description: The function format_file formats/strips a blocklist to our liking
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/SimpleRegexRemoval.py
# --i _Input_File_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

# Core
from pathlib import Path
import argparse
import logging
import os
import re
import sys

# Helpers

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

BLOCKLIST_TXT = Path(Data.SOURCES_PATH) / "blocklist.txt"
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
# SECTION: Create our functions
# ---------------------------------

# Does not support recursion
def simple_regex(wregx: str, exclusion_char: str = '/', force_match_all: bool = False) -> str:
    if not exclusion_char:
        raise ValueError('Missing `exclusion_char`.')

    tokens = []  # Initialize.
    regex = re.escape(wregx)  # Escape the input word/phrase
    exclusion_char = re.escape(exclusion_char)

    # Convert `$seq$` into `[seq]` for pure regex.
    def replace_seq(m):
        seq = m.group(1)
        seq = re.sub(r'([a-z0-9])\\-([a-z0-9])', r'\1-\2', seq)
        tokens.append(f'[{seq}]')  # Save token.
        return f'|%#%|{len(tokens) - 1}|%#%|'

    # Handle sequences without recursion
    regex = re.sub(r'\$\$([^$]+)\$', replace_seq, regex)

    # Convert `{this,that}` into `(?:this|that)` for pure regex.
    def replace_alternation(m):
        return '(?:' + re.sub(r'\{|}|,', lambda x: '|' if x.group(0) == ',' else '(', m.group(1)) + ')'

    regex = re.sub(r'\{([^{}]+)\}', replace_alternation, regex)

    if not force_match_all:
        regex = re.sub(r'\^', '^', regex)
        regex = re.sub(r'\$', '$', regex)

    def replace_question_marks(m):
        return f'[^{exclusion_char}]{{{len(m.group(0).replace("\\", ""))}}}'

    regex = re.sub(r'(?:\?){3,}', replace_question_marks, regex)
    regex = re.sub(r'(?:\?){2}', r'[\s\S]', regex)
    regex = re.sub(r'(?:\*){2,}', r'[\s\S]*?', regex)
    regex = re.sub(r'\?', f'[^{exclusion_char}]', regex)
    regex = re.sub(r'\*', f'[^{exclusion_char}]*?', regex)

    for i in reversed(range(len(tokens))):
        regex = regex.replace(f'|%#%|{i}|%#%|', tokens[i])

    return f'^{regex}$' if force_match_all else f'{regex}'

def remove_phrases_from_file(file_path: str, phrases_to_remove: list, exclusion_char: str = '/') -> None:
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        total_removed = 0  # Initialize a counter for removed phrases

        # Create a regex pattern for each phrase to remove
        for phrase in phrases_to_remove:
            regex_pattern = simple_regex(phrase, exclusion_char)
            # Count occurrences before removal
            occurrences = len(re.findall(regex_pattern, content))
            total_removed += occurrences
            # Remove the phrase using regex
            content = re.sub(regex_pattern, '', content)

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        # Count the number of lines left after removal
        remaining_lines = content.splitlines()
        num_remaining_lines = len(remaining_lines)

        print(f"Successfully removed {total_removed} phrases from '{file_path}'.")
        print(f"Number of lines left after removal: {num_remaining_lines}")

    except FileNotFoundError as e:
        print(e)
    except PermissionError:
        print(f"Permission denied: Unable to access '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------
# python script_name.py path/to/your/file.txt "phrase1" "phrase2" --e "/"
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Remove specified phrases from a file.')
    parser.add_argument('--i', type=str, help='Path to the file from which to remove phrases.')
    parser.add_argument('--p', type=str, nargs='+', help='Phrases to remove from the file.')
    parser.add_argument('--e', type=str, default='/', help='Character to exclude in regex (default: /).')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    remove_phrases_from_file('/Volumes/Work/WebGit/dns-blocklists/Public/Matthew_16_18/NSFW/ATest.txt', ['sex', 'porn'])

    # Validate
    # if not args.i:
    #     print("Error: A file path must be provided.")
    #     return
    # if not args.p:
    #     print("Error: At least one phrase must be provided to remove.")
    #     return

    # Now call any routines
    # if args.i:
        # Validate input file
        # validate_input_file(args.i)
        # remove_phrases_from_file(args.i, args.p, args.e)

if __name__ == "__main__":
    main()
