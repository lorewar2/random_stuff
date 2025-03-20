import random
import os
from collections import defaultdict
import csv
import pysam

UNIQUE_CELLS = 400 # number of cells required
INCLUDE_DOUBLETS = False
BAR_CODE_MIN_READ = 8000 # Min number of reads corrosponding to cell
DONORS = 51
GET_FIRST_ONES_FAST = False
OUTPUT_BAM_PATH = "./all_comb.bam"
OUTPUT_BARCODES_PATH = "./all_comb.tsv"
SEED = 255

def main():
    random.seed(SEED)
    experiment_bams_selected = new_selection()
    combined_reads = defaultdict(list)
    # go through the bams and process them and what not
    for index, experiment_bam_path in enumerate(experiment_bams_selected):
        print("Processing -{} : {}".format(index, experiment_bam_path))
        if index not in [1,7,21,41]:
            continue
        sampled_reads = sample_bam_by_cb_tag(experiment_bam_path, UNIQUE_CELLS)
        if INCLUDE_DOUBLETS:
            modified_reads = modify_cb_tags_with_doublets(sampled_reads, "-{}".format(index), 0.01)
        else:
            modified_reads = modify_cb_tags(sampled_reads, "-{}".format(index))
        # put in combined reads
        # Iterate over each dictionary provided as input
        for key, value in modified_reads.items():
            # Append the value(s) for each key in the combined dictionary
            # If the value is a list (e.g., reads associated with a CB tag), extend it
            if isinstance(value, list):
                combined_reads[key].extend(value)
            else:
                combined_reads[key].append(value)
        save_modified_reads(combined_reads, "{}{}".format(OUTPUT_BAM_PATH, index), "{}{}".format(OUTPUT_BARCODES_PATH, index), experiment_bams_selected[1])
        combined_reads.clear()
    return

def modify_cb_tags_with_doublets(sampled_reads, modify_with, doublet_ratio_per_10_000_cells):
    doublet_ratio = doublet_ratio_per_10_000_cells
    number_of_cb_tags = len(sampled_reads.items())
    number_of_doublets_required = number_of_cb_tags * doublet_ratio
    doublet_cell_indices = []
    for i in range(number_of_doublets_required):
        doublet_cell_indices.append(random.randint(1, number_of_cb_tags))
    # Dictionary to store the modified sampled reads with updated CB tags
    modified_reads = {}
    doublet_modify_with = "-{}".format(random.randint(1, DONORS))
    for (index, (cb_tag, reads)) in enumerate(sampled_reads.items()):
        # check if this should be a doublet
        if index in doublet_cell_indices:
            # Modify the CB tag from ending with "-1" to "-2"
            if cb_tag.endswith("-1"):
                new_cb_tag = cb_tag[:-2] + modify_with + doublet_modify_with
            else:
                print(f"Warning: CB tag {cb_tag} does not end with '-1'. Skipping.")
                continue
            # Update the CB tag in each read
            modified_reads[new_cb_tag] = []
            for read in reads:
                # Create a copy of the read to avoid modifying the original object (if needed)
                read_copy = read
                # Update the "CB" tag within the read to match the new CB tag
                read_copy.set_tag("CB", new_cb_tag, value_type="Z")
                # Add the modified read to the new CB tag list
                modified_reads[new_cb_tag].append(read_copy)
        else:
            # Modify the CB tag from ending with "-1" to "-2"
            if cb_tag.endswith("-1"):
                new_cb_tag = cb_tag[:-2] + modify_with
            else:
                print(f"Warning: CB tag {cb_tag} does not end with '-1'. Skipping.")
                continue
            # Update the CB tag in each read
            modified_reads[new_cb_tag] = []
            for read in reads:
                # Create a copy of the read to avoid modifying the original object (if needed)
                read_copy = read
                # Update the "CB" tag within the read to match the new CB tag
                read_copy.set_tag("CB", new_cb_tag, value_type="Z")
                # Add the modified read to the new CB tag list
                modified_reads[new_cb_tag].append(read_copy)
    return modified_reads

def modify_cb_tags(sampled_reads, modify_with):
    # Dictionary to store the modified sampled reads with updated CB tags
    modified_reads = {}
    for cb_tag, reads in sampled_reads.items():
        # Modify the CB tag from ending with "-1" to "-2"
        if cb_tag.endswith("-1"):
            new_cb_tag = cb_tag[:-2] + modify_with
        else:
            print(f"Warning: CB tag {cb_tag} does not end with '-1'. Skipping.")
            continue
        # Update the CB tag in each read
        modified_reads[new_cb_tag] = []
        for read in reads:
            # Create a copy of the read to avoid modifying the original object (if needed)
            read_copy = read
            # Update the "CB" tag within the read to match the new CB tag
            read_copy.set_tag("CB", new_cb_tag, value_type="Z")
            # Add the modified read to the new CB tag list
            modified_reads[new_cb_tag].append(read_copy)
    return modified_reads

def new_selection():
    directories = [d for d in os.listdir("./") if os.path.isdir(os.path.join("./", d))]
    experiments_selected = []
    for dir in directories:
        temp_string = "./{}/possorted_genome_bam.bam".format(dir)
        experiments_selected.append(temp_string)
    print(experiments_selected)
    return experiments_selected

def select_the_bam_and_barcodes_to_process():
    experiments_selected = []
    # Get  a list of doners (manual cause there are other folders :C)
    donor_BL = ["BL{}".format(d) for d in range(1, 8)]
    donor_CB = ["CB{}".format(d) for d in range(1, 12)]
    donor_BM = ["BM{}".format(d) for d in range(1, 8)]
    donors = [entry for entry in (donor_BL + donor_CB + donor_BM)]

    # loop through the list and choose the one with highest umi/cell count
    for donor_index, donor in enumerate(donors):
        print("processing donor {} - {}".format(donor_index, donor))
        # get the subdirectories
        donor_experiments = list_subdirectories(donor)
        umi_to_cell = [0] * len(donor_experiments)
        # go through the experments and update umi list and select max
        for experiment_index, experiment in enumerate(donor_experiments):
            # get the umi to cell for this experiment
            experiment_metric_csv_path = "./{}/{}/outs/metrics_summary.csv".format(donor, experiment)
            try:
                # Open the CSV file
                #print(experiment_metric_csv_path)
                with open(experiment_metric_csv_path, mode='r', newline='') as csvfile:
                    # Read the CSV file
                    reader = csv.reader(csvfile)
                    # Skip the header row
                    _ = next(reader)
                    # Read the next row, which contains the values
                    values = next(reader)
                    # Get the last value in the row
                    print(int(values[-1].replace(',','')))
                    umi_to_cell[experiment_index] = int(values[-1].replace(',',''))
            except:
                print("0")
        print(umi_to_cell)
        max_index = umi_to_cell.index(max(umi_to_cell))
        selected_experiment = donor_experiments[max_index]
        print(max_index, selected_experiment)
        experiments_selected.append("./{}/{}/outs/possorted_genome_bam.bam".format(donor, selected_experiment))
    experiments_selected.sort()
    print(experiments_selected)
    return experiments_selected

def list_subdirectories(directory_path):
    try:
        # List only directories within the specified path
        subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
        return subdirectories
    except FileNotFoundError:
        return "The specified directory does not exist."
    except PermissionError:
        return "Permission denied for the specified directory."
    
def sample_bam_by_cb_tag(bam_file_path, num_unique_cbs):
    # Dictionary to store reads grouped by unique CB tags
    cb_dict = defaultdict(list)
    if GET_FIRST_ONES_FAST: # Get the first found cb tags
        unique_cb_tags = []
        with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
            # Iterate through all reads in the BAM file
            for read in bam_file.fetch():
                if read.has_tag("CB"):  # Check if read has "CB" tag
                    cb_tag = read.get_tag("CB")
                    if (cb_tag not in unique_cb_tags) and (len(cb_dict[cb_tag]) > BAR_CODE_MIN_READ):
                        if len(unique_cb_tags) >= num_unique_cbs:
                            break
                        unique_cb_tags.append(cb_tag)
                    cb_dict[cb_tag].append(read)
        # Create a dictionary for the sampled reads by CB tag
        sampled_reads = {cb: cb_dict[cb] for cb in unique_cb_tags}
        return sampled_reads
    else:   # go through all save them and get some random
        with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
            # Iterate through all reads in the BAM file
            for read in bam_file.fetch():
                if read.has_tag("CB"):  # Check if read has "CB" tag
                    cb_tag = read.get_tag("CB")
                    cb_dict[cb_tag].append(read)
        # Populate unique cbs with cbs which have more than BAR_CODE_MIN_READ reads
        unique_cbs = []
        for key in cb_dict.keys():
            if len(cb_dict[key]) > BAR_CODE_MIN_READ:
                unique_cbs.append(key)
            total_length = 0
            for read in cb_dict[key]:
                total_length += len(read)
            print("Total length ", total_length)
        # Get the first num_unique_cbs which are greater than BAR_CODE_MIN_READ
        # Totally random
        if len(unique_cbs) < num_unique_cbs:
            print(f"The BAM file only has {len(unique_cbs)} unique CB tags with > BAR_CODE_MIN_READ reads, less than the requested {num_unique_cbs}.")
            selected_cbs = unique_cbs  # Select all available unique CB tags
        else:
            # Randomly select the specified number of unique CB tags
            selected_cbs = random.sample(unique_cbs, num_unique_cbs)
        # Create a dictionary for the sampled reads by CB tag
        sampled_reads = {cb: cb_dict[cb] for cb in selected_cbs}
        return sampled_reads

def save_modified_reads(modified_reads, output_bam_path, output_barcodes_path, template_path):
    # Get the list of unique CB tags
    unique_cb_tags = list(modified_reads.keys())
    # Open a new BAM file for writing
    bamfile = pysam.AlignmentFile(template_path, "rb")
    with pysam.AlignmentFile(output_bam_path, "wb", template=bamfile) as out_bam:
        # Write each read to the output BAM file
        for cb_tag, reads in modified_reads.items():
            for read in reads:
                out_bam.write(read)
    # Write the unique CB tags to a barcodes.tsv file
    with open(output_barcodes_path, "w") as barcode_file:
        for cb_tag in unique_cb_tags:
            barcode_file.write(f"{cb_tag}\n")

if __name__ == "__main__":
    main()