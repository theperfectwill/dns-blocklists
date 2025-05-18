# ---------------------------------
# Script Name: Data.py
# Version: 1.0.0.0
# Description:
# Author: ThePerfectWill
# Usage: Not to be called directly
# ---------------------------------

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

# Version
PYTHON_VER = "python3"

# ID
FOLDER_NAME = "ThisFolderName"
VERSION = "1.0.0.0"

# Paths
SCRIPTS_PATH = "Code/Scripts"
FINAL_PATH = "Final"
NSFW_PATH = "NSFW"
RULES_PATH = "Regex/Rules"
SORTED_PATH = "Regex/Sorted"
SOURCES_PATH = "Sources"

# Files
UpdateStrings_py=f"{SCRIPTS_PATH}/UpdateStrings.py"
DownloadRepoLinks_py=f"{SCRIPTS_PATH}/DownloadRepoLinks.py"
RunPreHostlistCompiler_py=f"{SCRIPTS_PATH}/RunPreHostlistCompiler.py"
FormatLists_py=f"{SCRIPTS_PATH}/FormatLists.py"
Alphabetical_py=f"{SCRIPTS_PATH}/Alphabetical.py"
SortByRegexPatterns_py=f"{SCRIPTS_PATH}/SortByRegexPatterns.py"
GetCommonPhrases_py=f"{SCRIPTS_PATH}/GetCommonPhrases.py"
CombinePatternRules_py=f"{SCRIPTS_PATH}/CombinePatternRules.py"
RunFinalHostlistCompiler_py=f"{SCRIPTS_PATH}/RunFinalHostlistCompiler.py"

# File header comments
TITLE_COMMENT=f"! Title: RegexDNSF {FOLDER_NAME}"
DESC_COMMENT=f"! Description: My description here..."
HOMEPAGE_COMMENT=f"! Homepage: https://github.com/theperfectwill/dns-regex-filters"
VERSION_COMMENT=f"! Version: {VERSION}"
LICENSE_COMMENT=f"! License: https://github.com/theperfectwill/dns-regex-filters/blob/main/LICENSE"
ISSUES_COMMENT=f"! Issues: https://github.com/theperfectwill/dns-regex-filters/issues"
EXPIRES_COMMENT=f"! Expires: 1 day"
LAST_MOD_COMMENT=f"! Last modified:"
ORIGINAL_RULE_COUNT_COMMENT=f"! Original rule count:"
CURRENT_RULE_COUNT_COMMENT=f"! Current rule count:"
RULE_REDUCED_COUNT_COMMENT=f"! Reduced rule notes:"
RULE_REDUCTION_NOTES_COMMENT=f"! -- See \"Source: Regex/Rules/combined.txt\" in this file for reference."
SYNTAX_COMMENT=f"! Syntax: Adblock"
AUTHOR_COMMENT=f"! Author: ThePerfectWill"
COMPILED_COMMENT=f"! Compiled by @adguard/hostlist-compiler"

# Logging
# Calling in files: logging.basicConfig(**Data.LOG)
# Usage in functions: logging.info(f"Successfully executed: {script}")
LOG = {
    # 'level': 'INFO',  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    # 'filename': '.log',  # Set log file separately
    # 'filemode': 'a'  # Optional: append mode
}
