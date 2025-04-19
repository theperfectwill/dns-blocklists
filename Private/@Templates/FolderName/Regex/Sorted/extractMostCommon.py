# Description:
#
# Author: ThePerfectWill
# Version: 1.0
#
# Usage:
#     python3 $thisPythonFile $fileToCheck $numPhraseLength $numTopPhraseAmount $resultOutputFile

from collections import Counter
import re
import argparse

def get_most_common_phrases(file_path, phrase_length=2, top_n=100):
    # List of words to exclude
    tlds = {
        'com', 'org', 'net', 'edu', 'gov', 'mil', 'info', 'io', 'co', 'biz',
        'me', 'us', 'uk', 'ca', 'de', 'jp', 'fr', 'au', 'it', 'es', 'ru',
        'cn', 'in', 'br', 'mx', 'kr', 'nl', 'se', 'ch', 'no', 'fi', 'dk',
        'pl', 'za', 'at', 'be', 'hk', 'sg', 'tw', 'ae', 'cl', 'cz', 'pt',
        'ro', 'sk', 'th', 'tr', 'vn', 'ph', 'my', 'ng', 'sa', 'il', 'lt',
        'lv', 'ee', 'bg', 'hr', 'si', 'is', 'mt', 'lu', 'by', 'ua', 'kz',
        'am', 'ge', 'md', 'rs', 'ba', 'mk', 'al', 'cy'
    }

    exclude_words = {
        'x', 'top', 'w9'
    }

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Read and convert to lowercase

    # Use regex to find words and ignore punctuation
    words = re.findall(r'\b\w+\b', text)

    # Filter out excluded words
    words = [word for word in words if word not in tlds and word not in exclude_words]

    # Create phrases
    phrases = [' '.join(words[i:i + phrase_length]) for i in range(len(words) - phrase_length + 1)]

    # Count occurrences of each phrase
    phrase_counts = Counter(phrases)

    # Get the most common phrases
    most_common_phrases = phrase_counts.most_common(top_n)

    return most_common_phrases

def main():
    parser = argparse.ArgumentParser(description='Get the most common phrases from a text file.')
    parser.add_argument('file_path', type=str, help='Path to the input text file')
    parser.add_argument('phrase_length', type=int, help='Number of words in each phrase')
    parser.add_argument('top_n', type=int, help='Number of top phrases to display')
    parser.add_argument('output_file', type=str, help='Path to the output text file')

    args = parser.parse_args()

    try:
        most_common_phrases = get_most_common_phrases(args.file_path, args.phrase_length, args.top_n)

        # Write the results to the output file
        with open(args.output_file, 'w', encoding='utf-8') as out_file:
            out_file.write("Most Common Phrases:\n")
            for phrase, count in most_common_phrases:
                out_file.write(f"{phrase}: {count}\n")

        print(f"Results have been written to {args.output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
