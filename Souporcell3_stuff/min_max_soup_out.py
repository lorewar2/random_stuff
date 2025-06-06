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
    td_loss = [[] for _ in range(64)]
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            index += 1
            tabbed = line.strip().split("\t")
            if tabbed[0] == "binomial":
                thread = tabbed[1]
                loss = tabbed[-3]
                print(thread, loss)
                td_loss[int(thread)].append(loss)
    print(td_loss)
    td_loss.sort(key=lambda x: x[-1])
    print("best")
    for index, entry in enumerate(td_loss[0]):
        print ("{}\t{}".format(index, entry))
    print("median")
    for index, entry in enumerate(td_loss[31]):
        print ("{}\t{}".format(index, entry))
    print("worst")
    for index, entry in enumerate(td_loss[-1]):
        print ("{}\t{}".format(index, entry))
            

if __name__ == "__main__":
    main()