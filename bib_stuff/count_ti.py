import re

def count_titles(file_path):
    # Initialize a counter for the titles
    title_count = 0

    # Open the file and read line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Check if the line starts with "TI -"
            if line.startswith("TI"):
                title_count += 1

    return title_count

# Path to the file containing the entries
file_path = 'all_converted.txt'

# Get the count of TI tags
ti_count = count_titles(file_path)

# Print the result
print(f"Total number of TI tags: {ti_count}")