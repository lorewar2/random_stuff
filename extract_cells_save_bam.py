import pysam
import random
from collections import defaultdict

UNIQUE_CELLS = 10 # number of cells required
BAR_CODE_MIN_READ = 10 # Min number of reads corrosponding to cell
GET_FIRST_ONES_FAST = True
OUTPUT_BAM_PATH = "./test.bam"
OUTPUT_BARCODES_PATH = "./test.tsv"
SEED = 10

def main():
    random.seed(SEED)
    # Try for one bam first
    bam_file_path = "/data1/cellector/kmeans_pp/split_by_doner/CB1/MantonCB1_HiSeq_4/outs/possorted_genome_bam.bam"
    num_unique_cbs = UNIQUE_CELLS  # Number of unique CB tags to sample
    sampled_reads = sample_bam_by_cb_tag(bam_file_path, num_unique_cbs)
    # Print information about sampled reads
    for cb_tag, reads in sampled_reads.items():
        print(f"CB Tag: {cb_tag} {len(reads)}")
    # Modify the reads
    modified_reads = modify_cb_tags(sampled_reads)
    # save the modified
    save_modified_reads(modified_reads, OUTPUT_BAM_PATH, OUTPUT_BARCODES_PATH, bam_file_path)
        #for read in reads:
            #print(read)
    return

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

def modify_cb_tags(sampled_reads):
    # Dictionary to store the modified sampled reads with updated CB tags
    modified_reads = {}
    for cb_tag, reads in sampled_reads.items():
        # Modify the CB tag from ending with "-1" to "-2"
        if cb_tag.endswith("-1"):
            new_cb_tag = cb_tag[:-2] + "-2"
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