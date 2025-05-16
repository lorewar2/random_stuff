import os
import sys

NUM_CLUS = 71
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

def process_file(file_path):
    clus_info = [[0 for j in range(NUM_CLUS)] for i in range(NUM_CLUS)]
    entries = []
    print("Going through lines")
    index = 0
    with open(file_path, 'r') as file:
        for line in file:
            temp = line.strip().split("\t")[0].split("-")
            temp2 = line.strip().split("\t")[1]
            if len(temp) == 2 and temp2[0:5] == "donor":
                entries.append(line.strip())
            index += 1
            if index % 100 == 0:
                print("Current line ", index)

    for entry in entries:
        ground = int(entry.split("\t")[0].split("-")[1])
        prediction = int(entry.split("\t")[1][5:])
        clus_info[ground][prediction] += 1
    assignment = []
    duplicate_count = 0
    for index, info in enumerate(clus_info):
        if max(info) != 0:
            max_index = info.index(max(info))
            print(index, info.index(max(info)), info)
            if max_index not in assignment:
                assignment.append(max_index)
            else:
                print("duplicated")
                duplicate_count += 1
    print("duplicate count ", duplicate_count)
if __name__ == "__main__":
    main()