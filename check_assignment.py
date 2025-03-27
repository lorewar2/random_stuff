import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get file path from command-line argument
    process_file(file_path)

def process_file(file_path):
    print("Going through lines")
    index = 0
    prev_truth = 2500
    number_of_same = [0] * 85
    indices = []
    assigned_wrong = 0
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            tabbed = line.strip().split("\t")
            current_truth = tabbed[0].split("-")[1]
            if current_truth != prev_truth:
                print(number_of_same.index(max(number_of_same)))
                    #print("THIS IS BAD")
                if number_of_same.index(max(number_of_same)) not in indices:
                    indices.append(number_of_same.index(max(number_of_same)))
                else:
                    if number_of_same.index(max(number_of_same)) != 0:
                        print("already in array", number_of_same.index(max(number_of_same)))
                    assigned_wrong += 1
                # print all stuff
                number_of_same.clear()
                number_of_same = [0] * 85
                prev_truth = current_truth
            else:
                number_of_same[int(tabbed[1])] += 1
            index += 1
            if index > 17_550:
                break
    print("wrong assignments ", assigned_wrong - 1)

if __name__ == "__main__":
    main()