import re

def convert_wos_to_scopus(input_file, output_file):
    # Define the WoS to Scopus field mappings
    field_mapping = {
        'PT': 'Document Type',           # Publication Type
        'AU': 'Authors',                 # Authors (initials and last names)
        'AF': 'Author Names',            # Full author names
        'TI': 'Title',                   # Title of the paper
        'SO': 'Source title',            # Journal name
        'LA': 'Language',                # Language of the paper
        'DT': 'Document Type',           # Document Type
        'DE': 'Keywords',                # Keywords
        'ID': 'Indexed keywords',        # Additional keywords
        'AB': 'Abstract',                # Abstract content
        'C1': 'Authors with affiliations', # Author addresses
        'C3': 'Affiliations',            # Country affiliations
        'RP': 'Correspondence Address',  # Corresponding author’s address
        'EM': 'Email Address',           # Corresponding author’s email
        'RI': 'Researcher ID',           # Researcher IDs
        'OI': 'ORCID',                   # ORCID IDs
        'FU': 'Funding Details',         # Funding information
        'FX': 'Funding Text',            # Funding acknowledgment text
        'CR': 'References',              # Cited references
        'NR': 'Cited Reference Count',   # Number of cited references
        'TC': 'Times Cited',             # Number of times cited
        'Z9': 'Total Times Cited',       # Total times cited (different sources)
        'U1': 'Usage Count (180 days)',  # Usage in the last 180 days
        'U2': 'Usage Count (Since 2013)', # Usage since 2013
        'PU': 'Publisher',               # Publisher information
        'PI': 'Publisher Location',      # Publisher’s location
        'PA': 'Publisher Address',       # Publisher’s address
        'SN': 'ISSN',                    # ISSN number
        'EI': 'E-ISSN',                  # Electronic ISSN
        'J9': 'Journal Abbreviation',    # Journal abbreviation
        'JI': 'ISO Source',              # ISO Source abbreviation
        'PD': 'Publication Date',        # Publication date
        'PY': 'Year',                    # Publication year
        'VL': 'Volume',                  # Volume number
        'IS': 'Issue',                   # Issue number
        'BP': 'Start Page',              # Beginning page
        'EP': 'End Page',                # Ending page
        'DI': 'DOI',                     # Digital Object Identifier
        'PG': 'Page Count',              # Total number of pages
        'WC': 'Subject Category',        # Web of Science subject category
        'SC': 'Research Areas',          # Research areas
        'GA': 'Document Identifier',     # Document identifier
        'UT': 'Unique Identifier',       # Web of Science identifier
        'PM': 'PubMed ID',               # PubMed identifier
    }

    # Initialize list to hold the converted entries for the final output
    scopus_entries = []
    current_data = {key: [] for key in field_mapping.values()}  # Map for holding the current entry's data

    # Helper function to reset current data
    def reset_current_data():
        for key in current_data:
            current_data[key] = []

    # Read the input file line by line
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Process each line
    for line in lines:
        # Ignore empty lines
        if line.strip() == "":
            # Consolidate each entry's tags into a single string and add to scopus_entries
            entry = []
            for scopus_tag, contents in current_data.items():
                if contents:
                    entry.append(f"{scopus_tag}: {'; '.join(contents)}")

            # Add the entry to scopus_entries and reset for the next entry
            scopus_entries.append("\n".join(entry))
            reset_current_data()
            continue

        # Split the line into WoS tag and content
        if ' ' in line[:4]:  # Only split if there's space after the tag
            tag, content = line[:2].strip(), line[3:].strip()
        else:
            continue

        # Map WoS tags to Scopus tags, if tag exists in the mapping
        if tag in field_mapping:
            scopus_tag = field_mapping[tag]
            if scopus_tag in current_data:
                current_data[scopus_tag].append(content)

    

    # Write all Scopus-formatted entries to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(scopus_entries))

    print(f"Conversion to Scopus format completed! Output saved to: {output_file}")

# Example usage
input_file = 'wos_original.txt'  # Replace with your WoS file path
output_file = 'wos_converted.txt'  # Desired output file path
convert_wos_to_scopus(input_file, output_file)
