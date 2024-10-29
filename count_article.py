def count_article_tags(file_path):
    # Initialize a counter for the @Article tags
    article_count = 0

    # Open the file and read line by line
    with open(file_path, 'r', encoding='latin1') as file:
        for line in file:
            # Check if the line starts with "@Article"
            if line.strip().startswith("@ARTICLE"):
                article_count += 1

    return article_count

# Path to the file containing the entries
file_path = 'scopus(2).bib'

# Get the count of @Article tags
article_count = count_article_tags(file_path)

# Print the result
print(f"Total number of @Article tags: {article_count}")