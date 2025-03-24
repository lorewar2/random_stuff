
def main():
    process_file("84_result.tsv")
    return

def process_file(file_path):
    print("Going through lines")
    index = 0
    prev_truth = 0
    number_of_same = [0] * 85
    with open(file_path, 'r') as file:
        # Read all lines from the f
        for line in file:
            tabbed = line.strip().split("\t")
            current_truth = tabbed[0].split("-")[1]
            if current_truth != prev_truth:
                print(prev_truth, " ", max(number_of_same))
                # print all stuff
                prev_truth = current_truth
            else:
                number_of_same[int(tabbed[1])] += 1
            index += 1
            if index % 100 == 0:
                print("Current line ", index)        

if __name__ == "__main__":
    main()