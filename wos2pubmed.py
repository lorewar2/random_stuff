import re

def convert_wos_to_pubmed(input_file, output_file):
    # Define WoS to PubMed field mappings
    field_mapping = {
        'PT': 'PT',                 # Publication Type
        'AU': 'AU',                # Authors (initials and last names)
        'AF': 'FAU',                 # Full author names
        'TI': 'TI',                 # Title
        'SO': 'JT',                 # Journal Title
        'LA': 'LA',                 # Language
        'DT': 'PT',                 # Document Type
        'DE': 'MH',                 # Mesh Headings (Keywords)
        'ID': 'OT',                 # Other Terms (additional keywords)
        'AB': 'AB',                 # Abstract
        'C1': 'AD',                 # Affiliation
        'RP': 'AD',                 # Correspondence Address
        'EM': 'AID',                # Email Address
        'RI': 'RID',                # Researcher ID
        'OI': 'OID',                # ORCID ID
        'FU': 'GR',                 # Grant
        'FX': 'GRNT',               # Grant Text
        'CR': 'RF',                 # References
        'NR': 'RN',                 # Cited Reference Count
        'TC': 'CIN',                # Times Cited in WoS
        'U1': 'UIN',                # Unique ID
        'U2': 'UIN',                # Unique ID
        'PU': 'PL',                 # Publisher
        'PI': 'PL',                 # Publisher Location
        'PA': 'PL',                 # Publisher Address
        'SN': 'IS',                 # ISSN number
        'EI': 'IS',                 # E-ISSN
        'J9': 'ISO',                # ISO Source
        'JI': 'JT',                 # ISO Source abbreviation
        'PD': 'DP',                 # Publication Date
        'PY': 'YR',                 # Year
        'VL': 'VI',                 # Volume
        'IS': 'IP',                 # Issue
        'BP': 'PG',                 # Beginning Page
        'EP': 'PG',                 # Ending Page
        'DI': 'LID',                # DOI (Link ID)
        'WC': 'MHDA',               # Subject Category
        'SC': 'MHDA',               # Research Area
        'GA': 'OID',                # Document Identifier
        'UT': 'PMID',               # PubMed Identifier
        'PM': 'PMID',               # PubMed ID
    }
    
    # Initialize list to hold the converted entries for the final output
    pubmed_entries = []
    current_data = {key: [] for key in field_mapping.values()}  # Map for holding the current entry's data

    # Helper function to reset current data
    def reset_current_data():
        for key in current_data:
            current_data[key] = []

    # Read the input file line by line
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Initialize current_tag for line continuation tracking
    current_tag = None

    # Process each line
    for line in lines:
        # Ignore empty lines
        if line.strip() == "":
            # Consolidate each entry's tags into a single string and add to pubmed_entries
            entry = []
            for pubmed_tag, contents in current_data.items():
                if contents:
                    # Formatting as PubMed expects, with each field on a new line
                    for content in contents:
                        length = len(pubmed_tag)
                        count = 4 - length
                        if count == 0:
                            entry.append(f"{pubmed_tag}- {content}")
                        if count == 1:
                            entry.append(f"{pubmed_tag} - {content}")
                        if count == 2:
                            entry.append(f"{pubmed_tag}  - {content}")
                        if count == 3:
                            entry.append(f"{pubmed_tag}   - {content}")
                    
            # Add the entry to pubmed_entries and reset for the next entry
            pubmed_entries.append("\n".join(entry))
            reset_current_data()
            continue

        # Split the line into WoS tag and content
        if ' ' in line[:4]:  # Only split if there's space after the tag
            tag, content = line[:2].strip(), line[3:].strip()
        else:
            continue

        # Map WoS tags to PubMed tags, if tag exists in the mapping
        if tag in field_mapping:
            pubmed_tag = field_mapping[tag]

            # Handle multiple entries separated by semicolons
            split_content = [item.strip() for item in content.split(';')]

            # Append each split content as a separate entry in the PubMed format
            if pubmed_tag in current_data:
                current_data[pubmed_tag].extend(split_content)


    

    # Write all PubMed-formatted entries to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(pubmed_entries))

    print(f"Conversion to PubMed format completed! Output saved to: {output_file}")

# Example usage
input_file = 'wos_original.txt'  # Replace with your WoS file path
output_file = 'wos_converted2.txt'  # Desired output file path
convert_wos_to_pubmed(input_file, output_file)
