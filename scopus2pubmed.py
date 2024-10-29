import re

def convert_bibtex_to_pubmed(bibtex_entry):
    pubmed_entry = []

    # Extract required fields from the BibTeX entry using regex
    pmid = "[Placeholder for PMID]"
    journal = re.search(r'journal = {(.+?)}', bibtex_entry).group(1) if re.search(r'journal = {(.+?)}', bibtex_entry) else ""
    volume = re.search(r'volume = {(.+?)}', bibtex_entry).group(1) if re.search(r'volume = {(.+?)}', bibtex_entry) else ""
    issue = re.search(r'number = {(.+?)}', bibtex_entry).group(1) if re.search(r'number = {(.+?)}', bibtex_entry) else ""
    year = re.search(r'year = {(.+?)}', bibtex_entry).group(1) if re.search(r'year = {(.+?)}', bibtex_entry) else ""
    title = re.search(r'title = {(.+?)}', bibtex_entry).group(1) if re.search(r'title = {(.+?)}', bibtex_entry) else ""
    doi = re.search(r'doi = {(.+?)}', bibtex_entry).group(1) if re.search(r'doi = {(.+?)}', bibtex_entry) else ""
    abstract = re.search(r'abstract = {(.+?)}', bibtex_entry, re.DOTALL).group(1) if re.search(r'abstract = {(.+?)}', bibtex_entry, re.DOTALL) else ""
    author_keywords = re.search(r'author_keywords = {(.+?)}', bibtex_entry).group(1) if re.search(r'author_keywords = {(.+?)}', bibtex_entry) else ""

    # Compile the PubMed entry
    pubmed_entry.append(f"PMID- {pmid}")
    pubmed_entry.append("OWN - NLM")
    pubmed_entry.append("STAT- MEDLINE")
    pubmed_entry.append("IS  - 2223-7747 (Electronic)")  # Assuming ISSN, modify as needed
    pubmed_entry.append(f"VI  - {volume}")
    pubmed_entry.append(f"IP  - {issue}")
    pubmed_entry.append(f"DP  - {year}")
    pubmed_entry.append(f"TI  - {title}")
    pubmed_entry.append("PG  - [Page range, if available]")
    pubmed_entry.append(f"LID - {doi} [doi]")
    pubmed_entry.append(f"AB  - {abstract}")
    # Add author keywords, each prefixed with OT
    keywords_list = author_keywords.split("; ")
    for keyword in keywords_list:
        pubmed_entry.append(f"OT  - {keyword}")
    # Join all lines into a single PubMed-style entry
    pubmed_entry_text = "\n".join(pubmed_entry)
    return pubmed_entry_text

def read_file_to_array(file_path, encoding='utf-8'):
    # Initialize an empty list to hold the entries
    entries = []
    
    # Open the file in read mode with specified encoding
    with open(file_path, 'r', encoding=encoding) as file:
        current_entry = []

        for line in file:
            # Check if the line is empty
            if line.strip() == "":
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
file_path = 'scopus(2).bib'  # Replace with your file path
output_file = "scopus_converted.txt"
entries = read_file_to_array(file_path, encoding='latin-1')  # You can change this if needed
for i, entry in enumerate(entries):
    if i == 0:
        continue
    with open(output_file, 'a', encoding='latin-1') as f:
        f.write("{}\n\n".format(convert_bibtex_to_pubmed(entry)))

