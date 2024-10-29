import re

import re

def convert_scopus_to_wos(scopus_entry):
    # Prepare storage for WoS entry
    wos_entry = []

    # Extract fields from Scopus format
    authors = re.search(r'AUTHOR FULL NAMES: (.+?)\n', scopus_entry).group(1)
    author_ids = re.findall(r'\d+', authors)
    title = re.search(r'\n([^\n]+)\n\(\d{4}\)', scopus_entry).group(1)
    journal_year = re.search(r'\((\d{4})\)', scopus_entry).group(1)
    journal_name = re.search(r'\(\d{4}\) (.+?), \d+,', scopus_entry).group(1)
    volume = re.search(r', (\d+), art', scopus_entry).group(1)
    doi = re.search(r'DOI: (.+)', scopus_entry).group(1)
    affiliations = re.search(r'AFFILIATIONS: (.+?)ABSTRACT', scopus_entry, re.DOTALL).group(1).strip()
    abstract = re.search(r'ABSTRACT: (.+?)AUTHOR KEYWORDS', scopus_entry, re.DOTALL).group(1).strip()
    author_keywords = re.search(r'AUTHOR KEYWORDS: (.+?)INDEX KEYWORDS', scopus_entry, re.DOTALL).group(1).strip()
    index_keywords = re.search(r'INDEX KEYWORDS: (.+?)FUNDING DETAILS', scopus_entry, re.DOTALL).group(1).strip()
    funding_text = re.search(r'FUNDING TEXT [0-9]: (.+?)(?=REFERENCES|CORRESPONDENCE)', scopus_entry, re.DOTALL).group(1).strip()
    issn = re.search(r'ISSN: (.+)', scopus_entry).group(1)
    language = re.search(r'LANGUAGE OF ORIGINAL DOCUMENT: (.+)', scopus_entry).group(1)
    authors_separated = authors.split(";")
    author_entry = authors_separated[0].split("(")[0]
    # Format WoS fields
    wos_entry.append(f"AU {author_entry}")  # Format each author on new line
    index = 0
    for author in authors_separated:
        index += 1
        if index == 1:
            continue
        author_entry = author.split("(")[0]
        wos_entry.append(f"  {author_entry}")
    wos_entry.append(f"AF {author_entry}")  # Full author names
    index = 0
    for author in authors_separated:
        index += 1
        if index == 1:
            continue
        author_entry = author.split("(")[0]
        wos_entry.append(f"  {author_entry}")
    wos_entry.append(f"TI {title}")
    wos_entry.append(f"SO {journal_name}")
    wos_entry.append(f"VL {volume}")
    wos_entry.append(f"PY {journal_year}")
    wos_entry.append(f"DI {doi}")
    wos_entry.append(f"AB {abstract}")
    wos_entry.append(f"DE {author_keywords.replace('; ', '; ')}")  # WoS uses "DE" for author keywords
    wos_entry.append(f"ID {index_keywords.replace('; ', '; ')}")  # WoS uses "ID" for index keywords
    wos_entry.append(f"FU {funding_text}")
    wos_entry.append(f"SN {issn}")
    wos_entry.append(f"LA {language}")
    # Combine into WoS format
    wos_entry_text = "\n".join(wos_entry)
    return wos_entry_text


def read_file_to_array(file_path, encoding='utf-8'):
    # Initialize an empty list to hold the entries
    entries = []
    
    # Open the file in read mode with specified encoding
    with open(file_path, 'r', encoding=encoding) as file:
        current_entry = []

        for line in file:
            # Check if the line has start source
            if line.strip().split(":")[0] == "SOURCE":
                # If current_entry is not empty, add it to entries
                if current_entry:
                    entries.append("".join(current_entry).strip())
                    current_entry = []  # Reset for the next entry
            else:
                # Append non-empty line to current_entry
                current_entry.append(line)

        # Add the last entry if the file does not end with an empty line
        if current_entry:
            entries.append("".join(current_entry).strip())

    return entries

# Example usage
file_path = 'scopus.txt'  # Replace with your file path
output_file = "scopus_converted.txt"
entries = read_file_to_array(file_path, encoding='utf-8')  # You can change this if needed
for i, entry in enumerate(entries):
    print(convert_scopus_to_wos(entry))
    break

    #with open(output_file, 'a', encoding='utf-8') as f:
        #f.write("{}\n\n".format(convert_bibtex_to_pubmed(entry)))

