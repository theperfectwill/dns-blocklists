#!/bin/bash

# Script Name: update.sh
# Description: This script performs our updates.
# Note: This update many times requires manual reviewing to view new possible keywords.
# Author: ThePerfectWill
# Usage: chmod +x ./update.sh && ./update.sh

# Import our variables
source ../vars.txt

# Signal our task start
echo "START: Updating $FolderName Keywords"
echo

# Set our variables
linksFile="links.txt"
keywordFile="keywords.txt"

# Check that our files exist
if [ -z "$linksFile" ] || [ -z "$keywordFile" ]; then
    echo "Usage: $0 $linksFile $keywordFile"
    exit 1
fi

# Create our createKeywordList function
function createKeywordList() {

    # Clearing $keywordFile
    echo "Clearing $keywordFile"
    >"$keywordFile"
    echo

    # Concatenating to $keywordFile
    echo "Concatenating $linksFile to $keywordFile"
    wget -q -O - -i <(grep -v '^#' $linksFile) >>$keywordFile
    echo

    # Sorting $keywordFile
    echo "Sorting $keywordFile"
    sort -o $keywordFile $keywordFile
    echo

}

# Call our createKeywordList function
# createKeywordList

# Create our filterKeyword function
function filterKeyword() {

    # Set our local variables
    local keywordFile="$1"

    # Run our hostlistcompiler for Keywords/$keywordFile keywords
    echo "Running hostlist-compiler for Keywords/$keywordFile.json to Keywords/$keywordFile.txt"
    echo
    hostlist-compiler -c Keywords/$keywordFile.json -o Keywords/$keywordFile.txt
    echo

    # Remove empty line comments
    sed -i.tmp '/^!$/d' Keywords/$keywordFile.txt && rm -f Keywords/$keywordFile.txt.tmp

    # Sort our output saving the first 4 comment lines
    { head -n 4 Keywords/$keywordFile.txt && sed '1,4d' Keywords/$keywordFile.txt | sort; } >"Keywords/$keywordFile.txt.tmp" && mv Keywords/$keywordFile.txt.tmp Keywords/$keywordFile.txt

}

# Create our filterKeywords function
function filterKeywords() {

    # Call our filterKeyword routines
    filterKeyword "hyphen"
    filterKeyword "numberRepeat"
    filterKeyword "numberSingle"
    filterKeyword "space"
    filterKeyword "special"
    filterKeyword "underscore"
    filterKeyword "wordRepeat"
    filterKeyword "wordSingle"

}

# Call our filterKeywords function
# filterKeywords

# Signal task end
echo "END: Updated $FolderName Keywords"
