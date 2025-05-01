# ---------------------------------
# Script Name: DownloadRepoLinks.py
# Version: 1.0.0.0
# Description: Downloads content from valid URLs listed in sourceLinks.txt and appends it to sourceDownloads.txt
# Author: ThePerfectWill
# Usage: python3 DownloadRepoLinks.py
# ---------------------------------

# ---------------------------------
# SECTION: Set our external references
# ---------------------------------

# Core
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import logging
import os
import re
import sys

# Helpers
import requests

# Custom
sys.path.append(os.path.join(os.getcwd(), 'Code', 'Scripts'))
import _Vars

# ---------------------------------
# SECTION: Misc. (Logs, Debugging, Execution Time, Directory Checks, etc.)
# ---------------------------------

logging.basicConfig(**_Vars.LOG)

# ---------------------------------
# SECTION: Set our variables and constants
# ---------------------------------

links_file = os.path.join(_Vars.SOURCES_PATH, "sourceLinks.txt")
source_file = os.path.join(_Vars.SOURCES_PATH, "sourceDownloads.txt")
lock = Lock()

# ---------------------------------
# SECTION: Define our functions
# ---------------------------------

def create_source_directory():
    os.makedirs(_Vars.SOURCES_PATH, exist_ok=True)

def read_links(file_path):
    try:
        with open(file_path, "r") as f:
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

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'[A-F0-9]*:[A-F0-9:]+)'  # IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url)

def download_content(url):
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

def write_to_blocklist(content):
    with lock:  # Ensure thread-safe writing
        with open(source_file, "a") as f:
            f.write(content + "\n")

def download_content_from_links():
    create_source_directory()  # Ensure the source directory exists
    links = read_links(links_file)  # Read links from the file

    if not links:
        logging.warning("No links found to process.")
        return 0  # Return early if there are no links

    # Clear the content of sourceDownloads.txt before downloading new content
    with open(source_file, "w") as f:
        pass  # This clears the file

    successful_downloads = 0  # Counter for successful downloads

    # Use a thread pool to download content concurrently
    with ThreadPoolExecutor() as executor:
        # Submit download tasks for valid URLs
        future_to_url = {executor.submit(download_content, link): link for link in links if is_valid_url(link)}

        # Process the results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]  # Get the URL associated with the future
            content = future.result()  # Get the result of the download
            if content:
                write_to_blocklist(content)  # Write content to blocklist
                successful_downloads += 1  # Increment successful download count

    return successful_downloads  # Return the number of successful downloads

# ---------------------------------
# SECTION: Call our main function with our subfunctions
# ---------------------------------

def main():
    logging.info(f"Processed {download_content_from_links()} links.")

if __name__ == "__main__":
    main()
