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

import os

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def sort_keywords_to_files(input_file, output_dir):
    # Create a dictionary to hold lists of keywords for each letter
    keywords_dict = {chr(i): [] for i in range(ord('A'), ord('Z') + 1)}

    # Read the input file and sort keywords into the dictionary
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Check if the line is not empty
                first_letter = line[0].upper()  # Get the first letter and convert to uppercase
                if first_letter in keywords_dict:
                    keywords_dict[first_letter].append(line)

    # Write the sorted keywords to separate files in the specified output directory
    for letter, keywords in keywords_dict.items():
        if keywords:  # Only create a file if there are keywords for that letter
            output_file = os.path.join(output_dir, f"{letter}.txt")
            with open(output_file, 'w') as file:
                for keyword in sorted(keywords):  # Sort keywords alphabetically
                    file.write(keyword + '\n')

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

if __name__ == "__main__":
    # Predefined paths
    input_file = 'Regex/Sorted/keywords.txt'  # Specify the input file name
    output_dir = 'Regex/Sorted/Letters'      # Specify the output directory path

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    sort_keywords_to_files(input_file, output_dir)
    print(f"Sorted keywords have been written to {output_dir}.")
