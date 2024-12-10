import random
import os
from collections import defaultdict
import csv
import pysam

SEED = 10
INPUT_FILE_PATH = "1000_cell.bam"
OUTPUT_PATH = "1000_with_doublets.bam"
DOUBLET_PERCENT = 1

def main():
    random.seed(SEED)
    cb_dict, doublet_dics_by_donor  = read_all_bam_files()
    doublet_list = make_a_doublet_list(doublet_dics_by_donor)
    # Write to BAM the doublets
    return

def make_a_doublet_list(doublet_dics_by_donor):
    # Combine pairs until doubet dict is empty
    doublet_dics_by_donor_empty = False
    list_with_doublets = []
    while doublet_dics_by_donor_empty == False:
        # Select 2 donors and 1 cell from each
        two_selected_donors = random.sample(range(len(doublet_dics_by_donor)), 2)
        cell_to_remove_1 = random.sample(list(doublet_dics_by_donor[two_selected_donors[0]].keys()), 1)
        cell_to_remove_2 = random.sample(list(doublet_dics_by_donor[two_selected_donors[1]].keys()), 1)
        # Append the reads
        appended_reads = doublet_dics_by_donor[two_selected_donors[0]][cell_to_remove_1] + doublet_dics_by_donor[two_selected_donors[1]][cell_to_remove_2]
        cell_bar_code = random.choice([cell_to_remove_1, cell_to_remove_2])
        combined_donors_string = "-{}-{}".format(two_selected_donors[0], two_selected_donors[1])
        # change the cb tag on appended reads
        for read in appended_reads:
            # Create a copy of the read to avoid modifying the original object (if needed)
            read_copy = read
            # Update the "CB" tag within the read to match the new CB tag
            new_cb_tag = cell_bar_code[:-2] + combined_donors_string
            read_copy.set_tag("CB", new_cb_tag, value_type="Z")
        list_with_doublets.append((combined_donors_string, cell_bar_code, appended_reads))
        # Remove the cells from doublet_dics_by_donor
        del doublet_dics_by_donor[two_selected_donors[0]][cell_to_remove_1]
        del doublet_dics_by_donor[two_selected_donors[1]][cell_to_remove_2] 
        if len(doublet_dics_by_donor[two_selected_donors[0]]) < 2:
            del doublet_dics_by_donor[two_selected_donors[0]]
        if len(doublet_dics_by_donor[two_selected_donors[1]]) < 2:
            del doublet_dics_by_donor[two_selected_donors[1]]
        # Update doublet_dics_by_donor_empty
        current_number_of_cells = sum([len(dics) for dics in doublet_dics_by_donor])
        if current_number_of_cells < 5 or len(doublet_dics_by_donor) < 3:
            doublet_dics_by_donor_empty = True
    return list_with_doublets

def read_all_bam_files():
    combined_reads = defaultdict(list)
    doublet_by_donor = []
    for index in range(27):
        donor_doublets = defaultdict(list)
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
                donor_doublets[key].extend(value)
            else:
                donor_doublets[key].append(value)
        doublet_by_donor.append(donor_doublets)
    return (combined_reads, doublet_by_donor)
