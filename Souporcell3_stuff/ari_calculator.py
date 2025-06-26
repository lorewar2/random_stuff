
import sys
import os
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

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
            if len(temp) == 2 and line.strip().split("\t")[1][0:5] == "donor":
                entries.append(line.strip())
                # get the ground truth cluster
                ground_truth_cluster = int(line.strip().split("\t")[0].split("-")[1])
                cluster_ground.append(ground_truth_cluster)
            # get the soupercell cluster
                soupurcell_cluster = int(line.strip().split("\t")[1][5:])
                #soupurcell_cluster = int(line.strip().split("\t")[1])
                cluster_method.append(soupurcell_cluster)
            elif len(temp) == 2:
                cluster_ground.append(0)
                cluster_method.append(1)
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