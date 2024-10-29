# Open the file and read it line by line
with open('all_converted.txt', 'r', encoding='utf-8') as file:
    count = 0
    line_counter = 0

    # Initialize a flag to check if "review" has been found in the current group of 10 lines
    found_in_group = False

    # Loop through each line in the file
    for line in file:
        line_counter += 1  # Increment line counter
        
        # Check if the word "review" (case-insensitive) is in the line
        if "review" in line.lower():
            found_in_group = True  # Set the flag if "review" is found in the current group
        
        # Check if we've processed 10 lines
        if line_counter % 20 == 0:
            if found_in_group:
                count += 1  # Increment count for this group if "review" was found
                found_in_group = False  # Reset the flag for the next group

    # Handle any remaining lines if the total number of lines isn't a multiple of 10
    if line_counter % 10 != 0 and found_in_group:
        count += 1

print(f"The word 'review' appears once every 10 lines in {count} instances in the file.")