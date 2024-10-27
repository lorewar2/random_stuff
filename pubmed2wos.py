def convert_pubmed_to_wos(input_file, output_file):
    # Define field mapping for the required fields
    field_mapping = {
        'PT': 'PT',      # Publication Type
        'AU': 'AU',      # Authors with initials
        'FAU': 'AF',     # Full Author Names
        'TI': 'TI',      # Title
        'TA': 'SO',      # Journal Source
        'LA': 'LA',      # Language
        'PT': 'DT',      # Document Type
        'OT': 'DE',      # Keywords
        'ID': 'ID',      # Identifier keywords
        'AB': 'AB',      # Abstract
        'AD': 'C1',      # Author Address
        'PL': 'C3',      # Country of publication
        'PMID': 'PM',    # PubMed ID
        'DP': 'PY',      # Year of publication
        'VI': 'VL',      # Volume
        'IP': 'IS',      # Issue
        'PG': 'PG',      # Page
        'LID': 'DI',     # DOI
    }

    # To hold the processed entries for the final output
    wos_entries = []

    # Initialize variables
    current_data = {key: [] for key in field_mapping.values()}
    
    # Function to reset current_data
    def reset_current_data():
        for key in current_data:
            current_data[key] = []

    # Read the input file
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    index = 0
    for line in lines:
        if line.strip() == "":
            index += 1
            print("empty", index)
            continue  # Skip empty lines

        # Split the line into tag and content
        if '- ' in line:
            tag, content = line.split('- ', 1)
            tag = tag.strip()
            content = content.strip()
        else:
            # Handle line continuation
            if current_data and current_data:
                current_data[wos_tag][-1] += " " + line.strip()
            continue

        # Map and append to respective fields
        if tag in field_mapping:
            wos_tag = field_mapping[tag]
            if wos_tag == "TI":
                print(wos_tag)
            current_data[wos_tag].append(content)

    # Consolidate all fields into single strings, separated by semicolons or line breaks as needed
    entry = []
    for wos_tag, contents in current_data.items():
        if contents:
            separator = "; " if wos_tag != 'AU' and wos_tag != 'AF' else "\n   "
            entry.append(f"{wos_tag} {separator.join(contents)}")

    # Add to final entries and reset for the next entry
    wos_entries.append("\n".join(entry))
    reset_current_data()

    # Write all formatted entries to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(wos_entries))

    print(f"Conversion to WoS format completed! Output saved to: {output_file}")

# Example usage
input_file = 'pubmed_original.txt'  # Replace with your input file path
output_file = 'pubmed_converted.txt' # Desired output file path
convert_pubmed_to_wos(input_file, output_file)
