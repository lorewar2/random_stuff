import random
import os
from collections import defaultdict
import csv
import pysam

SEED = 10
INPUT_FILE_PATH = "1000_cell.bam"
OUTPUT_PATH = "1000_with_doublets.bam"
def main():
    random.seed(SEED)
    cb_dict, doublet_dict  = read_all_bam_files()
    # combine pairs until doubet dict is empty
    while len(doublet_dict) <= 1:
        print(1)
        # select 2
        cells_to_remove = random.sample(list(doublet_dict.keys()), 2)
        appended_reads = doublet_dict[cells_to_remove[0]] + doublet_dict[cells_to_remove[1]]
        combined_key = "{}{}"
        for cell in cells_to_remove:
            del doublet_dict[cell]
        # take 
    for index, (key, value) in enumerate(doublet_dict):
       print(index)
    return

def read_all_bam_files():
    combined_reads = defaultdict(list)
    combined_doublets = defaultdict(list)
    for index in range(27):
        bam_file_path = "{}{}".format(INPUT_FILE_PATH, index)
        cb_dict = defaultdict(list)
        with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
            # Iterate through all reads in the BAM file
            for read in bam_file.fetch():
                if read.has_tag("CB"):  # Check if read has "CB" tag
                    cb_tag = read.get_tag("CB")
                    cb_dict[cb_tag].append(read)
        # Select 1% of the barcodes for doublets
        percent_1_size = len(cb_dict) / 100
        # Randomly select cells to remove
        cells_to_remove = random.sample(list(cb_dict.keys()), percent_1_size)
        # Save the removed key-value pairs
        temp_doublets = {cell: cb_dict[cell] for cell in cells_to_remove}
        # Delete the entries from the original dictionary
        for cell in cells_to_remove:
            del cb_dict[cell]
        # Create a dictionary for the sampled reads by CB tag
        for key, value in cb_dict.items():
            # Append the value(s) for each key in the combined dictionary
            # If the value is a list (e.g., reads associated with a CB tag), extend it
            if isinstance(value, list):
                combined_reads[key].extend(value)
            else:
                combined_reads[key].append(value)
        # Create a dictionary for the sampled reads by CB tag
        for key, value in temp_doublets.items():
            # Append the value(s) for each key in the combined dictionary
            # If the value is a list (e.g., reads associated with a CB tag), extend it
            if isinstance(value, list):
                combined_doublets[key].extend(value)
            else:
                combined_doublets[key].append(value)
    return (combined_reads, combined_doublets)
