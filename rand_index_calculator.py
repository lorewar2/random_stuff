# Randindex calculator for soupercell output
#a {\displaystyle a}, the number of pairs of elements in S {\displaystyle S} that are in the same subset in X {\displaystyle X} and in the same subset in Y {\displaystyle Y}
#b {\displaystyle b}, the number of pairs of elements in S {\displaystyle S} that are in different subsets in X {\displaystyle X} and in different subsets in Y {\displaystyle Y}
#c {\displaystyle c}, the number of pairs of elements in S {\displaystyle S} that are in the same subset in X {\displaystyle X} and in different subsets in Y {\displaystyle Y}
#d {\displaystyle d}, the number of pairs of elements in S {\displaystyle S} that are in different subsets in X {\displaystyle X} and in the same subset in Y {\displaystyle Y}
    
def main():
    file_path = 'random_clusters_tmp.tsv'  # Path to your file
    process_file(file_path)
    return

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
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            entries.append(line.strip())
            index += 1
            if index % 100 == 0:
                print("Current line ", index)        
    print("Read the file")
    randindex_variables = [0, 0, 0, 0] # abcd
    for i in range(len(entries)):
        print("processing {} out of {}, current result {}".format(i, len(entries), randindex_variables))
        for j in range(i + 1, len(entries)):  
            received_index = process_pair(entries[i], entries[j])
            randindex_variables[received_index] += 1
    print("Final variables ", randindex_variables)
    # print the result
    print((randindex_variables[0] + randindex_variables[1]) / sum(randindex_variables))
if __name__ == "__main__":
    main()