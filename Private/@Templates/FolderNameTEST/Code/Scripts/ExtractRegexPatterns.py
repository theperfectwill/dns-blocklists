# ---------------------------------
# Script Name: fileNameHere.sh
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage:
#  python3
# ---------------------------------

# ---------------------------------
# SECTION: Set our class imports
# ---------------------------------

import os
import re

# Create the necessary directories
if not os.path.exists("Regex"):
    os.makedirs("Regex")
if not os.path.exists("Regex/Sorted"):
    os.makedirs("Regex/Sorted")
if not os.path.exists("Regex/Sorted/DomainParents"):
    os.makedirs("Regex/Sorted/DomainParents")
if not os.path.exists("Regex/Sorted/DomainChildren"):
    os.makedirs("Regex/Sorted/DomainChildren")
if not os.path.exists("Regex/Sorted/OnlyLetters"):
    os.makedirs("Regex/Sorted/OnlyLetters")
if not os.path.exists("Regex/Sorted/Conjoined"):
    os.makedirs("Regex/Sorted/Conjoined")
if not os.path.exists("Regex/Sorted/WildCards"):
    os.makedirs("Regex/Sorted/WildCards")
if not os.path.exists("Regex/Sorted/OnlyNumbers"):
    os.makedirs("Regex/Sorted/OnlyNumbers")

# Extract matches and save them to the respective files
try:
    with open("Sources/blocklist.txt", "r") as file:
        lines = file.readlines()

    # Extract matches for the first regex pattern
    domain_parents = []
    for line in lines:
        match = re.search(r"\b([|]?)([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})([|^]?)(?=\s|$)", line)
        if match:
            domain_parents.append(match.group())
    with open("Regex/Sorted/DomainParents/extracts.txt", "w") as file:
        file.write("\n".join(domain_parents))

    # Extract matches for the second regex pattern
    domains_children = []
    for line in lines:
        match = re.search(r"^(?![a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", line)
        if match:
            domains_children.append(match.group())
    with open("Regex/Sorted/DomainChildren/extracts.txt", "w") as file:
        file.write("\n".join(domains_children))

    # Extract matches for the third regex pattern
    only_letters = []
    for line in lines:
        match = re.search(r"^[A-Za-z]+$", line)
        if match:
            only_letters.append(match.group())
    with open("Regex/Sorted/OnlyLetters/extracts.txt", "w") as file:
        file.write("\n".join(only_letters))

    # Extract matches for the fourth regex pattern
    spaces_underscores_hyphens = []
    for line in lines:
        match = re.search(r"^([a-zA-Z]+([ _-][a-zA-Z]+){0,99998})?$", line)
        if match:
            spaces_underscores_hyphens.append(match.group())
    with open("Regex/Sorted/Conjoined/extracts.txt", "w") as file:
        file.write("\n".join(spaces_underscores_hyphens))

    # Extract matches for the fifth regex pattern
    wildcards = []
    for line in lines:
        match = re.search(r"^.*\*.*$", line)
        if match:
            wildcards.append(match.group())
    with open("Regex/Sorted/WildCards/extracts.txt", "w") as file:
        file.write("\n".join(wildcards))

    # Extract matches for the sixth regex pattern
    only_numbers = []
    for line in lines:
        match = re.search(r"^[0-9]+
