import pandas as pd
import os

# Replace 'your_file.tsv' with the path to your TSV file
file_path = 'HCA.tsv'

# Read the TSV file
df = pd.read_csv(file_path, sep='\t')

pd.set_option('display.max_rows', None)
# Display the contents of the DataFrame
print(df.columns)
#df_bam = df[df["file_format"] == "bam"]
print(df[["donor_organism.biomaterial_core.biomaterial_id", "donor_organism.sex", "file_format", "file_name"]])

for index, row in df.iterrows():
    print(row['donor_organism.biomaterial_core.biomaterial_id'], row['file_name'])
    newpath = row['donor_organism.biomaterial_core.biomaterial_id'] 
    if not os.path.exists(newpath):
        os.makedirs(newpath)