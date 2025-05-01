#!/bin/bash

# ---------------------------------
# Script Name: update.sh
# Version: 1.0
# Description: This script performs our updates.
# Note: This update many times requires manual reviewing to add new regex accodmodations.
# Note: This update script consists of functions so if needed, the function calls below can be disabled individually
# Author: ThePerfectWill
# Usage:
#  chmod +x ./update.sh && ./update.sh
# ---------------------------------

# ---------------------------------
# SECTION: START
# ---------------------------------

# Signal our task start
echo "START: Updating $FolderName"
echo

# ---------------------------------
# SECTION: Import our variables
# ---------------------------------

source vars.txt

# python3 Code/Scripts/cleanBlocklist.py

# python3 Code/Scripts/domainFragments.py Regex/Sorted/keywords.txt Regex/Sorted/DomainsPrimary/list.txt '\b([|]?)([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})([|^]?)(?=\s|$)'
# python3 Code/Scripts/domainFragments.py Regex/Sorted/keywords.txt Regex/Sorted/DomainsSecondary/list.txt '^(?![a-zA-Z0-9-]+\.[a-zA-Z]{2,}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'

# ---------------------------------
# SECTION: Create our functions
# ---------------------------------

# Create our updateVariables function
function updateVariables() {
    # Define the directory and the string to replace
    local oldString="FolderName"
    local newString="$FolderName"
    local files=("@Notes/instructions.md" "Final/regexDNSF.json" "Final/regexDNSF.txt" "Sources/blocklist.json" "Sources/whitelist.json")

    # Loop through each file
    for file in "${files[@]}"; do
        # Check if the file exists
        if [[ -f "$file" ]]; then
            # Use sed to replace the old string with the new string
            sed -i.tmp "s/$oldString/$newString/g" "$file" && rm -f "$file.tmp"
            echo "Updated $file"
        else
            echo "$file does not exist."
        fi
    done
    echo
}

# Create our createKeywordList function
function createKeywordList() {

    # Set our variables
    linksFile="$regexPath/$sortedPath/sourceLinks.txt"
    keywordsFile="$regexPath/$sortedPath/keywords.txt"
    keywordsCompiler="$regexPath/$sortedPath/keywords.json"

    local compile="$1"

    # Check that our files exist
    if [ -z "$linksFile" ] || [ -z "$keywordsFile" ]; then
        echo "Usage: $0 $linksFile $keywordsFile"
        exit 1
    fi

    # Clearing $keywordsFile
    echo "Clearing $keywordsFile"
    >"$keywordsFile"
    echo

    # Concatenating to $keywordsFile
    echo "Concatenating $linksFile to $keywordsFile"
    wget -q -O - -i <(grep -v '^#' $linksFile) >>$keywordsFile
    echo

    # Run our hostlistcompiler for $keywordsCompiler to $keywordsFile
    # @Note->for an entirely keyword base file (ie: no domains) then we do not want to run our compiler on that file
    if [[ "$compile" == "true" ]]; then
        echo "Running hostlist-compiler for $keywordsCompiler to $keywordsFile"
        echo
        hostlist-compiler -c $keywordsCompiler -o $keywordsFile
        echo
    fi

    # Sorting $keywordsFile
    echo "Sorting $keywordsFile"
    sort -o $keywordsFile $keywordsFile
    echo

    # Removing not needed lines (aiming to leave only lines that beging with | )
    echo "Removing not needed lines in $keywordsFile"
    sed -i.tmp '/^[!#:@*\/\.\-].*$/d' $keywordsFile && rm -f $keywordsFile.tmp # Beginning with !#:@*/.-
    sed -i.tmp '/^[0-9a-zA-Z].*$/d' $keywordsFile && rm -f $keywordsFile.tmp   # Beginning with a digit or letter
    echo

    # Removing beginning | and ending ^ in $keywordsFile
    echo "Removing pipes in $keywordsFile"
    sed -i.tmp 's/^|*//' $keywordsFile && rm -f $keywordsFile.tmp
    sed -i.tmp 's/\^.*$//' $keywordsFile && rm -f $keywordsFile.tmp
    sed -i.tmp 's/\$.*$//' $keywordsFile && rm -f $keywordsFile.tmp
    echo

}

# Create our filterKeyword function
function filterKeyword() {

    # Set our local variables
    local thisPath="$regexPath/$sortedPath/$keywordsPath"
    local keywordsFile="$regexPath/$sortedPath"
    local keywordFile="$thisPath/$1"

    # Check that our files exist
    if [ -z "$keywordsFile" ] || [ -z "$keywordFile.json" ] || [ -z "$keywordFile.txt" ]; then
        echo "Usage: $0 $keywordsFile $keywordFile.json $keywordFile.txt"
        exit 1
    fi

    # Run our hostlistcompiler for $keywordFile.json to $keywordFile.txt
    echo "Running hostlist-compiler for $keywordFile.json to $keywordFile.txt"
    echo
    hostlist-compiler -c $keywordFile.json -o $keywordFile.txt
    echo

    # Removing comment lines in $keywordFile.txt
    echo "Removing comment lines in $keywordFile.txt"
    sed -i.tmp '/^!.*$/d' $keywordFile.txt && rm -f $keywordFile.txt.tmp
    echo

}

# Create our extractCommonPhrases function
function extractCommonPhrases() {

    # Set our variables
    local thisPath="$regexPath/$sortedPath"
    local mostCommonFile="extract.py"

    # Call extract.py with our desired outputs
    echo "Running $mostCommonFile"
    echo

    python3 $mostCommonFile $thisPath/$keywordsPath/domainsPri.txt 1 1000 $thisPath/$keywordsPath/domainsPriCommon.txt
    sort -nr -o $thisPath/$keywordsPath/domainsPriCommon.txt $thisPath/$keywordsPath/domainsPriCommon.txt
    echo "Sorted $thisPath/$keywordsPath/domainsPriCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/domainsSub.txt 1 1000 $thisPath/$keywordsPath/domainsSubCommon.txt
    sort -nr -o $thisPath/$keywordsPath/domainsSubCommon.txt $thisPath/$keywordsPath/domainsSubCommon.txt
    echo "Sorted $thisPath/$keywordsPath/domainsSubCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/lettersALL.txt 1 1000 $thisPath/$keywordsPath/lettersALLCommon.txt
    sort -nr -o $thisPath/$keywordsPath/lettersALLCommon.txt $thisPath/$keywordsPath/lettersALLCommon.txt
    echo "Sorted $thisPath/$keywordsPath/lettersALLCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/numberALL.txt 1 1000 $thisPath/$keywordsPath/numberALLCommon.txt
    sort -nr -o $thisPath/$keywordsPath/numberALLCommon.txt $thisPath/$keywordsPath/numberALLCommon.txt
    echo "Sorted $thisPath/$keywordsPath/numberALLCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/spaceUH.txt 1 1000 $thisPath/$keywordsPath/spaceUHCommon.txt
    sort -nr -o $thisPath/$keywordsPath/spaceUHCommon.txt $thisPath/$keywordsPath/spaceUHCommon.txt
    echo "Sorted $thisPath/$keywordsPath/spaceUHCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/specialC.txt 1 1000 $thisPath/$keywordsPath/specialCCommon.txt
    sort -nr -o $thisPath/$keywordsPath/specialCCommon.txt $thisPath/$keywordsPath/specialCCommon.txt
    echo "Sorted $thisPath/$keywordsPath/specialCCommon.txt"

    python3 $mostCommonFile $thisPath/$keywordsPath/wildCards.txt 1 1000 $thisPath/$keywordsPath/wildCardsCommon.txt
    sort -nr -o $thisPath/$keywordsPath/wildCardsCommon.txt $thisPath/$keywordsPath/wildCardsCommon.txt
    echo "Sorted $thisPath/$keywordsPath/wildCardsCommon.txt"

    echo
}

# Create our filterKeywords function
function filterKeywords() {

    # Call our filterKeyword routines for domain based files
    filterKeyword "domainsPri"
    filterKeyword "domainsSub"

    # Call our filterKeyword routines for keyword based files
    filterKeyword "lettersALL"
    filterKeyword "numberALL"
    filterKeyword "spaceUH"
    filterKeyword "wildCards"
    filterKeyword "specialC"

}

# Create our sortKeywords functio
function sortKeywords() {
    python3 sort.py
}

# Create our buildCombinedFiles function
function buildCombinedFiles() {

    # Set our variables
    local linksFile="$sourcesPath/sourceLinks.txt"
    local blocklistFile="$sourcesPath/blocklist.txt"
    local whitelistFile="$sourcesPath/whitelist.txt"

    # Check that our files exist
    if [ -z "$linksFile" ] || [ -z "$blocklistFile" ] || [ -z "$whitelistFile" ]; then
        echo "Usage: $0 $linksFile $blocklistFile $whitelistFile"
        exit 1
    fi

    # Generate our $blocklistFile

    # Clearing $blocklistFile
    echo "Clearing $blocklistFile"
    >"$blocklistFile"
    echo

    # Concatenating to $blocklistFile
    echo "Concatenating $linksFile to $blocklistFile"
    wget -q -O - -i <(grep -v '^[#!]' $linksFile) >>$blocklistFile
    echo

    # Run our hostlistcompiler
    echo "Running hostlist-compiler for $sourcesPath/blocklist.json to $blocklistFile"
    echo
    hostlist-compiler -c $sourcesPath/blocklist.json -o $blocklistFile
    echo

    # Remove empty line comments
    sed -i.tmp '/^!$/d' $blocklistFile && rm -f $blocklistFile.tmp

    # Sort our output saving the first 4 comment lines
    { head -n 4 $blocklistFile && sed '1,4d' $blocklistFile | sort; } >"$blocklistFile.tmp" && mv $blocklistFile.tmp $blocklistFile

    # Generate our $whitelistFile

    # Clearing $whitelistFile
    echo "Clearing $whitelistFile"
    >"$whitelistFile"
    echo

    # Run our hostlistcompiler
    echo "Running hostlist-compiler for $sourcesPath/whitelist.json to $whitelistFile"
    echo
    hostlist-compiler -c $sourcesPath/whitelist.json -o $whitelistFile
    echo

    # Remove empty line comments
    sed -i.tmp '/^!$/d' $whitelistFile && rm -f $whitelistFile.tmp

    # Sort our output saving the first 4 comment lines
    { head -n 4 $whitelistFile && sed '1,4d' $whitelistFile | sort; } >"$whitelistFile.tmp" && mv $whitelistFile.tmp $whitelistFile

}

# Create our buildFinalFile function
function buildFinalFile() {

    # Set our variables
    local finalFile="$finalPath/regexDNSF.txt"

    # Check that our files exist
    if [ -z "$finalFile" ]; then
        echo "Usage: $0 $finalFile"
        exit 1
    fi

    # Clearing $finalFile
    echo "Clearing $finalFile"
    >"$finalFile"
    echo

    # Run our hostlistcompiler
    echo "Running hostlist-compiler for $finalPath/regexDNSF.json to $finalFile"
    echo
    hostlist-compiler -c $finalPath/regexDNSF.json -o $finalFile
    echo

    # Remove empty line comments
    sed -i.tmp '/^!.*$/d' $finalFile && rm -f $finalFile.tmp
    sed -i.tmp "1i\\
! Title: RegexDNSF $FolderName
" "$finalFile" && rm -f $finalFile.tmp

}

# ---------------------------------
# SECTION: Call our functions
# ---------------------------------

# ------------
# @Note->buildCombinedFiles is for seperating the blocklist from its whitelisted entries
# ..and including any custom blocklist or whitelist entires
# @Note->this runs first because some of our other functions reference the data created after we build our compiled files
# ------------

# Call our buildCombinedFiles function
# buildCombinedFiles

# ------------
# @Note->createKeywordList and filterKeywords is for creating a seperate, filtered, stripped blocklist
# ..from which we analyze to create regex and/or wildcard patterns to reduce the amount of blocklist entires
# ..and to aim blocking future similar domain calls, but this also is aimed at lighter files and potentially harder blocking
# ..therefore whitelisting is expected as needed, at least for now
# ------------

# Call our updateVariables function
# updateVariables

# Call our createKeywordList function
# createKeywordList true

# Call our filterKeywords function
# filterKeywords

# Call our sortKeywords function
# sortKeywords

# Call our extractCommonPhrases function
# extractCommonPhrases

# ------------
# @Note->buildFinalFile is for creating the final version including our approved regex patterns
# ..replacing standard blocked domain entires with single regex patterns that match them
# @Example->/(?:\.|-|\|\||^)(adserver)(?:\.|-)/ will block...
# adserver | adserver. .adserver .adserver. adserver- -adserver -adserver-
# ------------

# Call our buildFinalFile function
# buildFinalFile

# ---------------------------------
# SECTION: END
# ---------------------------------

# Signal task end
echo "END: Updated $FolderName"
