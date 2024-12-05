import random
import os
from collections import defaultdict
import csv
import pysam

SEED = 10
FILE_PATH = "1000_cell.bam"
OUTPUT_PATH = "1000_with_doublets.bam"
def main():
    random.seed(SEED)
    experiment_bams_selected = read_all_bam_files()
    combined_reads = defaultdict(list)
    # go through the bams and process them and what not
    for index, experiment_bam_path in enumerate(experiment_bams_selected):
       print(index)
    return

def read_all_bam_files():
    cb_dict = defaultdict(list)
    unique_cb_tags = []
    with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
        # Iterate through all reads in the BAM file
        for read in bam_file.fetch():
            if read.has_tag("CB"):  # Check if read has "CB" tag
                cb_tag = read.get_tag("CB")
                if (cb_tag not in unique_cb_tags):
                    unique_cb_tags.append(cb_tag)
                cb_dict[cb_tag].append(read)
    # Create a dictionary for the sampled reads by CB tag
    sampled_reads = {cb: cb_dict[cb] for cb in unique_cb_tags}
    return sampled_reads
