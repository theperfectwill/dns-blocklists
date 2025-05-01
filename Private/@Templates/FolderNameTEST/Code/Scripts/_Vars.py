# ---------------------------------
# Script Name: Vars.py
# Version: 1.0
# Description:
# Author: ThePerfectWill
# Usage: Not to be called directly
# ---------------------------------

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

FOLDER_NAME = "ThisFolderName"

SCRIPTS_PATH = "Code/Scripts"
FINAL_PATH = "Final"
RULES_PATH = "Regex/Rules"
SORTED_PATH = "Regex/Sorted"
SOURCES_PATH = "Sources"

LOG = {
    'level': 'INFO',  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    # 'filename': '.log',  # Set log file separately
    # 'filemode': 'a'  # Optional: append mode
}
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')