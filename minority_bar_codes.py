import sys
import os

MINORITY_REQUIRED = 50
MINORITY_DOUBLET_REQUIRED = 5

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

def process_file(file_path):
    print("Going through lines")
    index = 0
    entries = []
    doublets = []
    minority_len = 0
    doublet_len = 0
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            temp = line.strip().split("\t")[0].split("-")
            if len(temp) == 2:
                if int(temp[1]) == 0:
                    if minority_len < MINORITY_REQUIRED:
                        entries.append(line.strip())
                    minority_len += 1
                else:
                    entries.append(line.strip())
            if len(temp) == 3:
                if int(temp[1]) == 0 or int(temp[2]) == 0:
                    if doublet_len < MINORITY_DOUBLET_REQUIRED:
                        doublets.append(line.strip())
                    doublet_len += 1
                else:
                    doublets.append(line.strip())
            index += 1
            if index % 100 == 0:
                print("Current line ", index)
    print("Read the file")
    with open("data_mod.tsv", "w") as txt_file:
        for line in entries:
            txt_file.write(line + "\n")
        for line in doublets:
            txt_file.write(line + "\n")

if __name__ == "__main__":
    main()