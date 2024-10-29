import re
from collections import Counter

def process_entries(file_path):
    # Initialize variables to store titles
    titles = []

    # Read file and split entries by double newlines
    with open(file_path, 'r', encoding='utf-8') as file:
        entries = file.read().strip().split('\n\n')

    # Extract the TI (Title) tag value from each entry
    for entry in entries:
        title_match = re.search(r'TI\s+-\s+(.+)', entry)
        if title_match:
            titles.append(title_match.group(1).strip())

    # Count occurrences of each title
    title_counts = Counter(titles)
    
    # Calculate unique and duplicate title counts
    unique_titles = sum(1 for count in title_counts.values() if count == 1)
    duplicate_titles = sum(1 for count in title_counts.values() if count > 1)
    
    return unique_titles, duplicate_titles

# Path to the file containing the entries
file_path = 'all_converted.txt'

# Get counts of unique and duplicate titles
unique_count, duplicate_count = process_entries(file_path)

# Print results
print(f"Unique titles: {unique_count}")
print(f"Duplicate titles: {duplicate_count}")