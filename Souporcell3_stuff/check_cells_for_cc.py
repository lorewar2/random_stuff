import sys
import os

NUM_CLUS = 62

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

def process_file(file_path):
    clus_info = [[i, 0, 0.0, 0.0] for i in range(NUM_CLUS)]
    total_cell_count = 0
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            total_cell_count += 1
            tabbed_line = line.split("\t")
            cell_id = tabbed_line[0]
            assigned_clus = int(tabbed_line[1])
            probs = tabbed_line[2:]
            prob_sum = 0
            for index, prob in enumerate(probs):
                prob_sum += float(prob)
            mean = prob_sum / NUM_CLUS
            assigned_prob = float(probs[assigned_clus])
            clus_info[assigned_clus][1] += 1
            clus_info[assigned_clus][2] += assigned_prob
            clus_info[assigned_clus][3] += assigned_prob / mean
    print("divided by cell count")
    clus_info.sort(key=lambda x: x[3])
    for index, entry in enumerate(clus_info):
        print(index, entry)
    q1_index = int(len(clus_info) * 1 / 4)
    q3_index = int(len(clus_info) * 3 / 4)
    iqr = (clus_info[q3_index][3] - clus_info[q1_index][3]) * 1.5
    print(clus_info[q1_index][3] - iqr)
    print(clus_info[q3_index][3] + iqr)
    print(iqr)
    for index, entry in enumerate(clus_info):
        print(index, entry)
        if entry[3] < clus_info[q1_index][3] - iqr:
            print("below")
        if entry[3] > clus_info[q3_index][3] + iqr:
            print("above")
    return

if __name__ == "__main__":
    main()