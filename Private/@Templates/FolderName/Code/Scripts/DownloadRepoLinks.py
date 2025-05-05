# ---------------------------------
# Script Name: DownloadRepoLinks.py
# Version: 1.0.0.0
# Description: Downloads content from valid URLs listed in sourceLinks.txt and appends it to sourceDownloads.txt
# Author: ThePerfectWill
# Usage: python3 Code/Scripts/DownloadRepoLinks.py
# --i _Input_File_ --o _Output_File_ --ll ERROR
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
import argparse
import logging
import os
import re
import sys

# Helpers
import requests

# Custom
sys.path.append(str(Path.cwd() / 'Code' / 'Scripts')); import Data

# ---------------------------------
# SECTION: Set our constants
# ---------------------------------

INPUT_FILE = Path(Data.SOURCES_PATH) / "sourceLinks.txt"
OUTPUT_FILE = Path(Data.SOURCES_PATH) / "sourceDownloads.txt"
LOCK = Lock()

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

def setup_logging(logging_level: str) -> None:
    logging.basicConfig(level=logging_level, **Data.LOG)

def validate_input_file(input_file: str) -> None:
    if not Path(input_file).is_file():
        logging.error(f"The input file '{input_file}' does not exist.")
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

def validate_output_directory(output_dir: str) -> None:
    if not Path(output_dir).is_dir():
        logging.error(f"The output directory '{output_dir}' does not exist.")
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist.")

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def create_source_directory() -> None:
    os.makedirs(Path(Data.SOURCES_PATH), exist_ok=True)

def read_links(file_path: Path) -> list[str]:
    try:
        with file_path.open("r") as f:
            links = []
            group_lines = []  # List to collect group lines
            for line in f:
                stripped_line = line.strip()
                if stripped_line:  # Check if the line is not empty
                    if stripped_line.startswith("!") or stripped_line.startswith("#"):
                        # Collect the line without the first character
                        group_lines.append(stripped_line[1:].strip())
                    else:
                        links.append(stripped_line)
            if group_lines:  # Check if there are any group lines to print
                print("Downloading blocklists from:", ", ".join(group_lines))  # Join with commas
                print()
            return links
    except FileNotFoundError:
        logging.error(f"Error: File {file_path} does not exist.")
        return []
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

def is_valid_url(url: str) -> bool:
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'[A-F0-9]*:[A-F0-9:]+)'  # IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def download_content(url: str) -> str | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not response.text:
            logging.warning("Empty response from %s", url)
            return None
        logging.info("Successfully downloaded content from %s", url)
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error("Error downloading from %s: %s", url, e)
        return None

def write_to_blocklist(content: str) -> None:
    with LOCK:  # Ensure thread-safe writing
        with OUTPUT_FILE.open("a") as f:
            f.write(content + "\n")

def clean_downloaded_file() -> None:
    with LOCK:  # Ensure thread-safe reading and writing
        # Read the content of the output file
        with OUTPUT_FILE.open("r") as f:
            lines = f.readlines()

        # Use a set to track unique lines
        unique_lines = set()
        cleaned_lines = []

        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Only process non-empty lines
                if stripped_line not in unique_lines:
                    unique_lines.add(stripped_line)
                    cleaned_lines.append(stripped_line)

        # Write the cleaned unique lines back to the output file
        with OUTPUT_FILE.open("w") as f:
            f.write("\n".join(cleaned_lines) + "\n")

def download_content_from_links() -> int:
    create_source_directory()  # Ensure the source directory exists
    links = read_links(INPUT_FILE)  # Read links from the file

    if not links:
        logging.warning("No links found to process.")
        return 0  # Return early if there are no links

    # Clear the content of sourceDownloads.txt before downloading new content
    OUTPUT_FILE.write_text("")  # Clear the file

    downloaded_count = 0
    for link in links:
        if is_valid_url(link):
            content = download_content(link)
            if content:
                write_to_blocklist(content)
                downloaded_count += 1
        else:
            logging.warning("Invalid URL: %s", link)

    # Remove duplicates from the output file after all downloads
    clean_downloaded_file()

    return downloaded_count

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Read links from a file and download their content to a specified output file')
    parser.add_argument('--i', '--input_file', type=str, default=INPUT_FILE, help='Input link file (default: sourceLinks.txt)')
    parser.add_argument('--o', '--output_file', type=str, default=OUTPUT_FILE, help='Output file for data downloaded (default: sourceDownloads.txt)')
    parser.add_argument('--ll', '--log_level', type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )

    args = parser.parse_args()

    # Define logging settings
    setup_logging(args.ll)

    # Validate our inputs and outputs
    validate_input_file(args.i)
    validate_output_directory(args.o)

    # Now call any routines
    logging.info(f"Processed {download_content_from_links()} links.")

if __name__ == "__main__":
    main()
