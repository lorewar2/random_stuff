
import sys
import os
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

# Function to process a pair of entries
def process_pair(entry1, entry2):
    a = False
    b = False
    c = False
    d = False
    index = 0
    entry1_ground, entry1_calc = get_soupurcell_cluster_and_ground_truth(entry1)
    entry2_ground, entry2_calc = get_soupurcell_cluster_and_ground_truth(entry2)
    # check if both equal
    if (entry1_ground == entry2_ground) and (entry1_calc == entry2_calc):
        a = True
        index = 0
    if (entry1_ground != entry2_ground) and (entry1_calc != entry2_calc):
        b = True
        index = 1
    if (entry1_ground == entry2_ground) and (entry1_calc != entry2_calc):
        c = True
        index = 2
    if (entry1_ground != entry2_ground) and (entry1_calc == entry2_calc):
        d = True
        index = 3
    assert((a + b + c + d) == 1) # something very wrong
    return index

def get_soupurcell_cluster_and_ground_truth(entry):
    split_entry = entry.split("\t")
    # get the ground truth cluster
    ground_truth_cluster = int(split_entry[0].split("-")[1])
    # get the soupercell cluster
    soupurcell_cluster = int(split_entry[1])
    #cluster_vectors = [float(value) for (value, index) in enumerate(split_entry) if index > 1]
    return (ground_truth_cluster, soupurcell_cluster)

# Read entries from a file
def process_file(file_path):
    print("Going through lines")
    index = 0
    entries = []
    cluster_method = []
    cluster_ground = []
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            temp = line.strip().split("\t")[0].split("-")
            if len(temp) == 2:
                entries.append(line.strip())
                # get the ground truth cluster
                ground_truth_cluster = int(line.strip().split("\t")[0].split("-")[1])
                cluster_ground.append(ground_truth_cluster)
            # get the soupercell cluster
                soupurcell_cluster = int(line.strip().split("\t")[1])
                cluster_method.append(soupurcell_cluster)
            index += 1
            if index % 100 == 0:
                print("Current line ", index)
    print("Read the file")
    print(file_path)
    ari = adjusted_rand_score(cluster_ground, cluster_method)
    print("Final variables ", ari)
    # print the result
if __name__ == "__main__":
    main()