def process_todo_file(file_path: str, output_path: str = 'Processed_Todo.txt') -> None:
    """
    Processes a todo file by replacing spaces with '*' in lines that do not start with '!'
    and writes the results to a new file, keeping lines that start with '!' unchanged.

    Args:
        file_path (str): The path to the input todo file.
        output_path (str): The path to the output file (default is 'Processed_Todo.txt').
    """
    try:
        with open(file_path, 'r') as file:
            processed_lines = []
            for line in file:
                stripped_line = line.rstrip()  # Strip only the trailing whitespace
                if stripped_line.startswith('!'):
                    # Keep lines starting with '!' unchanged
                    processed_lines.append(stripped_line)
                else:
                    # Replace spaces with '*' for other lines
                    modified_line = stripped_line.replace(' ', '*')
                    processed_lines.append(modified_line)

        # Write processed lines to the output file
        with open(output_path, 'w') as output_file:
            output_file.write('\n'.join(processed_lines) + '\n')

        print(f"Processing complete. Check '{output_path}' for results.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Specify the path to your @Todo.txt file
todo_file_path = '@Todo.txt'
process_todo_file(todo_file_path)
