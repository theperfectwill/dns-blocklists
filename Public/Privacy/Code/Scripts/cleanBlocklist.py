import re

def clean_file(file_path):
    # Define the patterns for lines to remove
    remove_patterns = [
        r'^[#:*@\\.\-]',  # Lines starting with #, :, @, *, \, ., -
        # r'^\d',           # Lines starting with a digit
    ]
    
    # Read the file and filter lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Filter out unwanted lines
    filtered_lines = [
        line for line in lines 
        if not any(re.match(pattern, line) for pattern in remove_patterns)
    ]
    
    # Remove unwanted characters from remaining lines
    cleaned_lines = [re.sub(r'[|^$]', '', line) for line in filtered_lines]
    cleaned_lines = [re.sub(r'\$.*', '', line) for line in cleaned_lines]  # Use cleaned_lines here
    
    # Write the cleaned lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)

if __name__ == "__main__":
    # Specify the file path
    file_path = 'Sources/blocklist.txt'  # Change this to your actual file path
    clean_file(file_path)
