#!/bin/bash

# Script Name: update.sh
# Description: This script performs our updates.
# Note: This update many times requires manual reviewing to add new regex accodmodations.
# Author: ThePerfectWill
# Usage: chmod +x ./update.sh && ./update.sh

# Import our variables
source vars.txt

# Signal our task start
echo "START: Updating $FolderName"
echo

# Set our variables
linksFile="$sourcesPath/links.txt"
combinedFile="$sourcesPath/combined.txt"
finalFile="$finalPath/regexDNSF.txt"

# Check that our files exist
if [ -z "$linksFile" ] || [ -z "$combinedFile" ] || [ -z "$finalFile" ]; then
    echo "Usage: $0 $linksFile $combinedFile"
    exit 1
fi

# Clearing $combinedFile
echo "Clearing $combinedFile"
>"$combinedFile"
echo

# Concatenating to $combinedFile
echo "Concatenating $linksFile to $combinedFile"
wget -q -O - -i <(grep -v '^#' $linksFile) >>$combinedFile
echo

# Run our hostlistcompiler
echo "Running hostlist-compiler for $sourcesPath/settings.json to $combinedFile"
echo
hostlist-compiler -c $sourcesPath/settings.json -o $combinedFile
echo

# Remove empty line comments
sed -i.tmp '/^!$/d' $combinedFile && rm -f $combinedFile.tmp

# Sort our output saving the first 4 comment lines
{ head -n 4 $combinedFile && sed '1,4d' $combinedFile | sort; } >"$combinedFile.tmp" && mv $combinedFile.tmp $combinedFile

# Run our hostlistcompiler
echo "Running hostlist-compiler for $finalPath/settings.json to $finalFile"
echo
hostlist-compiler -c $finalPath/settings.json -o $finalFile
echo

# Remove empty line comments
sed -i.tmp '/^!$/d' $finalFile && rm -f $finalFile.tmp

# Remove certain lines (this is a duplicate for some reason)
sed -i.tmp '/^! Source: Sources\/combined\.txt$/d' $finalFile && rm -f $finalFile.tmp

# Signal task end
echo "END: Updated $FolderName"
