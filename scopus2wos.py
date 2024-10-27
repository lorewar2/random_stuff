import re

def parse_bibtex_to_wos(file_path):
    # Regex patterns to capture BibTeX entries and fields
    entry_pattern = re.compile(r"@(\w+)\{([^,]+),\n(.*?)\n\}", re.DOTALL)
    field_pattern = re.compile(r"\s*(\w+)\s*=\s*\{(.+?)\},", re.DOTALL)

    wos_entries = []

    # Read the BibTeX file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract entries from the BibTeX file
    entries = entry_pattern.findall(content)

    # Process each entry
    for entry_type, entry_id, fields in entries:
        # Extract fields within the entry
        field_data = dict(field_pattern.findall(fields))
        
        # Prepare WoS tags
        wos_entry = []
        wos_entry.append("PT J")  # Publication Type

        # Authors and Author Full Names
        if 'author' in field_data:
            authors = field_data['author'].replace("\n", "").split(" and ")
            # Only include authors if the name is in "Last, First" format
            author_tags = [
                f"{a.split(',')[0]}, {a.split(',')[1].strip()[0]}" 
                for a in authors if len(a.split(',')) > 1
            ]
            wos_entry.append("AU " + "\n   ".join(author_tags))
            wos_entry.append("AF " + "\n   ".join(authors))
        
        # Title
        title = field_data.get('title', '')
        wos_entry.append(f"TI {title}")

        # Source (Journal)
        journal = field_data.get('journal', '')
        wos_entry.append(f"SO {journal}")

        # Year
        year = field_data.get('year', '')
        wos_entry.append(f"PY {year}")

        # DOI
        doi = field_data.get('doi', '')
        if doi:
            wos_entry.append(f"DI {doi}")

        # Abstract - Placeholder if not present
        abstract = field_data.get('abstract', 'Abstract not available.')
        wos_entry.append(f"AB {abstract}")

        # Combine into a single WoS formatted entry
        wos_entries.append("\n".join(wos_entry))
    
    # Join all entries and return as a single formatted string
    return "\n\n".join(wos_entries)

# File path to the .bib file
file_path = 'scopus_original.bib'

# Run the conversion
wos_output = parse_bibtex_to_wos(file_path)

# Save output to a new file or print it
output_path = 'scopus_converted.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(wos_output)

print("Conversion completed! Output saved to:", output_path)
