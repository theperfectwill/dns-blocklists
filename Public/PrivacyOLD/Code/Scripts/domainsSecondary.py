# ---------------------------------
# Script Name: ddomainsSecondary.py
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3 domainsSecondary.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

import os
import re

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

def extractThisDomain(url):
    # Use regex to extract the secondary domain from a URL
    pattern = r'^(?![a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None

def main():
    input_file = 'keywords.txt'
    output_file = 'DomainsSecondary/list.txt'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    theseDomains = set()

    # Read the keywords from the input file
    with open(input_file, 'r') as f:
        for line in f:
            domain = extractThisDomain(line.strip())
            if domain:
                theseDomains.add(domain)

    # Write the secondary domains to the output file
    with open(output_file, 'w') as f:
        for domain in sorted(theseDomains):
            f.write(domain + '\n')

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

if __name__ == '__main__':
    main()
