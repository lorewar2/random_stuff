# Randindex calculator for soupercell output
#a {\displaystyle a}, the number of pairs of elements in S {\displaystyle S} that are in the same subset in X {\displaystyle X} and in the same subset in Y {\displaystyle Y}
#b {\displaystyle b}, the number of pairs of elements in S {\displaystyle S} that are in different subsets in X {\displaystyle X} and in different subsets in Y {\displaystyle Y}
#c {\displaystyle c}, the number of pairs of elements in S {\displaystyle S} that are in the same subset in X {\displaystyle X} and in different subsets in Y {\displaystyle Y}
#d {\displaystyle d}, the number of pairs of elements in S {\displaystyle S} that are in different subsets in X {\displaystyle X} and in the same subset in Y {\displaystyle Y}

import sys
import os

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
    # get the ground truth cluster
    ground_truth_cluster = int(entry.split("\t")[0].split("-")[1])
    # get the soupercell cluster
    soupurcell_cluster = int(entry.split("\t")[1][5:])
    #cluster_vectors = [float(value) for (value, index) in enumerate(split_entry) if index > 1]
    return (ground_truth_cluster, soupurcell_cluster)

# Read entries from a file
def process_file(file_path):
    print("Going through lines")
    index = 0
    entries = []
    unassigned = 0
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            temp = line.strip().split("\t")[0].split("-")
            temp2 = line.strip().split("\t")[1]
            if len(temp) == 2:
                if temp2[0:5] == "donor":
                    entries.append(line.strip())
                if  temp2 == "unassigned" or temp2 == "doublet":
                    unassigned += 1
            index += 1
    randindex_variables = [0, 0, 0, 0] # abcd
    error = 0
    for i in range(len(entries) + unassigned):
        for j in range(i + 1, len(entries) + unassigned):
            if i >= len(entries) or j >= len(entries):
                error += 1
            else:
                received_index = process_pair(entries[i], entries[j])
                randindex_variables[received_index] += 1
    print(file_path)
    print("Final variables ", randindex_variables)
    # print the result
    print(error)
    print((randindex_variables[0] + randindex_variables[1]) / (sum(randindex_variables) + error))
if __name__ == "__main__":
    main()