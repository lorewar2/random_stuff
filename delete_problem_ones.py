import pysam

INPUT_FILE = "./final.bam"
OUTPUT_BAM_PATH = "./final_modified.bam"

def main():
    reads = sample_bam(INPUT_FILE)
    write_the_reads(OUTPUT_BAM_PATH, INPUT_FILE, reads)
    return

# remove problem cells
def sample_bam(bam_file_path):
    # Dictionary to store reads grouped by unique CB tags
    reads = []
    with pysam.AlignmentFile(bam_file_path, "rb") as bam_file:
        # Iterate through all reads in the BAM file
        for read in bam_file.fetch():
            if read.has_tag("CB"):  # Check if read has "CB" tag
                cb_tag = read.get_tag("CB")
                donor_index = int(cb_tag.split("-")[1])
                if donor_index not in [1, 7, 21, 41]:
                    reads.append(read)
    return reads

def write_the_reads(bam_write_path, template_path, reads):
    bamfile = pysam.AlignmentFile(template_path, "rb")
    with pysam.AlignmentFile(bam_write_path, "wb", template=bamfile) as out_bam:
        # Write each read to the output BAM file
        for read in reads:
            out_bam.write(read)
    return

if __name__ == "__main__":
    main()