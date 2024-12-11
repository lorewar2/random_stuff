import random
import os
from collections import defaultdict
import csv
import pysam

SEED = 10
INPUT_FILE_PATH = "merged.sorted.bam"
OUTPUT_BAM_PATH = "350_with_doublets.bam"
OUTPUT_BAR_PATH = "350_with_doublets.tsv"
DOUBLET_PERCENT = 1

def main():
    random.seed(SEED)
    all_dics_by_donor, doublet_dics_by_donor  = read_all_bam_files()
    print("doublet", len(doublet_dics_by_donor))
    for index in range(25):
        print(index, len(doublet_dics_by_donor[index]))
    print("all", len(all_dics_by_donor))
    for index in range(25):
        print(index, len(all_dics_by_donor[index]))
    doublet_list = make_a_doublet_list(doublet_dics_by_donor)
    print("final doublet list len ", len(doublet_list))
    # Write to BAM the doublets
    save_modified_reads(all_dics_by_donor, doublet_list, OUTPUT_BAM_PATH, OUTPUT_BAR_PATH, INPUT_FILE_PATH)
    return

def save_modified_reads(all_list, doublet_list, output_bam_path, output_barcodes_path, template_path):
    # Get the list of unique CB tags
    unique_cb_tags = []
    # Open a new BAM file for writing
    bamfile = pysam.AlignmentFile(template_path, "rb")
    with pysam.AlignmentFile(output_bam_path, "wb", template=bamfile) as out_bam:
        # Write each read to the bam file
        for donor_index in range(25):
            unique_cb_tags.extend(list(all_list[donor_index].keys()))
            # all file
            for cb_tag, reads in all_list[donor_index].items():
                for read in reads:
                    out_bam.write(read)
        # doublet file
        for entry in doublet_list:
            unique_cb_tags.append(entry[1])
            for read in entry[2]:
                out_bam.write(read)
            
    # Write the unique CB tags to a barcodes.tsv file
    with open(output_barcodes_path, "w") as barcode_file:
        for cb_tag in unique_cb_tags:
            barcode_file.write(f"{cb_tag}\n")
            
def make_a_doublet_list(doublet_dics_by_donor):
    # Combine pairs until doubet dict is empty
    doublet_dics_by_donor_empty = False
    list_with_doublets = []
    while doublet_dics_by_donor_empty == False:
        # Select 2 donors and 1 cell from each
        print("length of donors before processing ", len(doublet_dics_by_donor))
        two_selected_donors = random.sample(range(len(doublet_dics_by_donor)), 2)
        print("donor 1 ", two_selected_donors[0], len(doublet_dics_by_donor[two_selected_donors[0]]), " donor 2 ", two_selected_donors[1], len(doublet_dics_by_donor[two_selected_donors[1]]))
        cell_to_remove_1 = random.sample(list(doublet_dics_by_donor[two_selected_donors[0]].keys()), 1)[0]
        cell_to_remove_2 = random.sample(list(doublet_dics_by_donor[two_selected_donors[1]].keys()), 1)[0]
        # Append the reads
        appended_reads = doublet_dics_by_donor[two_selected_donors[0]][cell_to_remove_1] + doublet_dics_by_donor[two_selected_donors[1]][cell_to_remove_2]
        cell_bar_code = random.choice([cell_to_remove_1, cell_to_remove_2])
        combined_donors_string = "-{}-{}".format(two_selected_donors[0], two_selected_donors[1])
        # change the cb tag on appended reads
        modified_reads = []
        for read in appended_reads:
            # Create a copy of the read to avoid modifying the original object (if needed)
            read_copy = read
            # Update the "CB" tag within the read to match the new CB tag
            new_cb_tag = cell_bar_code.split("-")[0] + combined_donors_string
            read_copy.set_tag("CB", new_cb_tag, value_type="Z")
            modified_reads.append(read_copy)
        list_with_doublets.append((combined_donors_string, new_cb_tag, modified_reads))
        # Remove the cells from doublet_dics_by_donor
        del doublet_dics_by_donor[two_selected_donors[0]][cell_to_remove_1]
        del doublet_dics_by_donor[two_selected_donors[1]][cell_to_remove_2] 
        print("check len for delete ", len(doublet_dics_by_donor[two_selected_donors[0]]))
        print("check len for delete ", len(doublet_dics_by_donor[two_selected_donors[1]]))
        if len(doublet_dics_by_donor[two_selected_donors[0]]) == 0:
            del doublet_dics_by_donor[two_selected_donors[0]]
            # deleted entry rearrange
            if two_selected_donors[0] < two_selected_donors[1]:
                two_selected_donors[1] -= 1
        if len(doublet_dics_by_donor[two_selected_donors[1]]) == 0:
            del doublet_dics_by_donor[two_selected_donors[1]]
        # Update doublet_dics_by_donor_empty
        current_number_of_cells = sum([len(dics) for dics in doublet_dics_by_donor])
        if current_number_of_cells < 5 or len(doublet_dics_by_donor) < 2:
            doublet_dics_by_donor_empty = True
    return list_with_doublets

def read_all_bam_files():
    doublet_by_donor = [defaultdict(list) for _ in range(25)]
    all_by_donor = [defaultdict(list) for _ in range(25)]
    bam_file_path = "{}".format(INPUT_FILE_PATH)
    index = 0
    with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
        # Iterate through all reads in the BAM file
        for read in bam_file.fetch():
            if read.has_tag("CB"):  # Check if read has "CB" tag
                cb_tag = read.get_tag("CB")
                donor_index = int(cb_tag.split("-")[1])
                all_by_donor[donor_index][cb_tag].append(read)
                index += 1
            if index % 1000 == 0:
                print(index)
            if index > 10_000_000:
                break
    print("retrieved all reads")
    print("Pre removeal")
    for index in range(25):
        print(index, len(all_by_donor[index]))
    # Go through each donor and select 1 percent from each
    for donor_index in range(25):
        # Select 1% of the barcodes for doublets
        percent_1_size = int(len(all_by_donor[donor_index]) / 100)
        print("1 percent doublet size", percent_1_size)
        # Randomly select cells to remove
        cells_to_remove = random.sample(list(all_by_donor[donor_index].keys()), percent_1_size)
        print("cells to remove size ", len(cells_to_remove))
        # Save the removed key-value pairs
        temp_doublets = {cell: all_by_donor[donor_index][cell] for cell in cells_to_remove}
        # Delete the entries from the original dictionary
        for cell in cells_to_remove:
            del all_by_donor[donor_index][cell]
        # Create a dictionary for the sampled reads by CB tag
        for key, value in temp_doublets.items():
            # Append the value(s) for each key in the combined dictionary
            # If the value is a list (e.g., reads associated with a CB tag), extend it
            if isinstance(value, list):
                doublet_by_donor[donor_index][key].extend(value)
            else:
                doublet_by_donor[donor_index][key].append(value)
    return (all_by_donor, doublet_by_donor)

if __name__ == "__main__":
    main()