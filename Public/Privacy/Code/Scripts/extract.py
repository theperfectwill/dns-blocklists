# ---------------------------------
# Script Name: extractCommon.sh
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3 $thisPythonFile $fileToCheck $numPhraseLength $numTopPhraseAmount $resultOutputFile
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

from collections import Counter
from pathlib import Path
import re
import os
import argparse

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def load_exclusions(filename):
    # Get the current working directory
    current_directory = Path.cwd()
    # Prepend "Regex/Sorted" to the current directory
    sorted_directory = current_directory / "Regex" / "Sorted"
    # Construct the full path to the exclusions file
    exclusions_path = os.path.join(sorted_directory, filename)

    with open(exclusions_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_most_common_phrases(file_path, phrase_length=2, amount=100):

    # List of words to exclude
    exclusions = load_exclusions('exclusions.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Read and convert to lowercase

    # Use regex to find words and ignore punctuation
    words = re.findall(r'\b\w+\b', text)

    # Filter out excluded words
    words = [word for word in words if word not in exclusions]

    # Create phrases
    phrases = [' '.join(words[i:i + phrase_length]) for i in range(len(words) - phrase_length + 1)]

    # Count occurrences of each phrase
    phrase_counts = Counter(phrases)

    # Get the most common phrases
    most_common_phrases = phrase_counts.most_common(amount)

    return most_common_phrases

def main():
    parser = argparse.ArgumentParser(description='Get the most common phrases from a text file.')
    parser.add_argument('file_path', type=str, help='Path to the input text file')
    parser.add_argument('phrase_length', type=int, help='Number of words in each phrase')
    parser.add_argument('amount', type=int, help='Number of top phrases to display')
    parser.add_argument('output_file', type=str, help='Path to the output text file')

    args = parser.parse_args()

    try:
        most_common_phrases = get_most_common_phrases(args.file_path, args.phrase_length, args.amount)

        # Write the results to the output file
        with open(args.output_file, 'w', encoding='utf-8') as out_file:
            # out_file.write("Most Common Phrases:\n") # @ToDo->remove uneccessary now
            for phrase, count in most_common_phrases:
                out_file.write(f"{count}: {phrase}\n")

        print(f"Results have been written to {args.output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

if __name__ == "__main__":
    main()
