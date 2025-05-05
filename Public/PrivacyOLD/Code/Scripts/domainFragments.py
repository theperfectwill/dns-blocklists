# ---------------------------------
# Script Name: domainsPrimary.py
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3 domainsPrimary.py keywords.txt DomainsPrimary/list.txt '^\b([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})(?=\s|$)'
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

import os
import re
import argparse

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def extract_domain_fragment(url, pattern):
    # Use regex to extract domain fragments from a URL
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None

def main(input_file, output_file, pattern):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    theseDomains = set()

    # Read the urls from the desired input file
    with open(input_file, 'r') as f:
        for line in f:
            domain = extract_domain_fragment(line.strip(), pattern)
            if domain:
                theseDomains.add(domain)

    # Write the domain fragments to the desired output file
    with open(output_file, 'w') as f:
        for domain in sorted(theseDomains):
            f.write(domain + '\n')

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract domain fragments from a list of URLs.')
    parser.add_argument('input_file', type=str, help='Enter file to analyze')
    parser.add_argument('output_file', type=str, help='Enter file/directory to save to')
    parser.add_argument('pattern', type=str, help='Enter regex pattern to extract by')

    args = parser.parse_args()

    main(args.input_file, args.output_file, args.pattern)
