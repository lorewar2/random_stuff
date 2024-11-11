# PROJECT 3 Python code Weerakoon

import hashlib  # used for SHA256
import re
import os

def main():
    image_name = "project3.dd"
    output_dir = "generated_files"
    PDF_start_end, GIF_start_end, JPG_start_end, AVI_start_end, PNG_start_end = find_signatures_clean_save(image_name)
    print_and_save_the_files(PDF_start_end, GIF_start_end, JPG_start_end, AVI_start_end, PNG_start_end, image_name, output_dir)

def find_signatures_clean_save(dd_file_path):
    # Patterns with wildcards (xx)
    wildcard_patterns = {
        "JPG_Start": b'\xFF\xD8\xFF\xE0..',       # JPG start with xx xx
        "AVI_Start": b'\x52\x49\x46\x46....'      # AVI start with xx xx xx xx
    }
    fixed_signatures = {
        # Fixed byte sequences
        "PDF_Start": b'\x25\x50\x44\x46',
        "PDF_End_1": b'\x0A\x25\x25\x45\x4F\x46',         # .%%EOF
        "PDF_End_2": b'\x0A\x25\x25\x45\x4F\x46\x0A',     # .%%EOF.
        "PDF_End_3": b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A', # ..%%EOF..
        "PDF_End_4": b'\x0D\x25\x25\x45\x4F\x46\x0D',     # .%%EOF.
        "GIF_Start_1": b'\x47\x49\x46\x38\x37\x61',       # GIF87a
        "GIF_Start_2": b'\x47\x49\x46\x38\x39\x61',       # GIF89a
        "GIF_End": b'\x00\x3B',                           # .;
        "JPG_End": b'\xFF\xD9',                           # JPG end
        "PNG_Start": b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', # PNG start
        "PNG_End": b'\x49\x45\x4E\x44\xAE\x42\x60\x82',    # PNG end
        "AVI_End": b'\x69\x64\x78\x31'
    }
    found_signatures = {name: [] for name in wildcard_patterns.keys() | fixed_signatures.keys()}
    # Open the .dd file in binary read mode
    with open(dd_file_path, 'rb') as f:
        # Read the entire file into memory
        file_data = f.read()
        # Search for each wildcard pattern in the file data using regex
        for name, pattern in wildcard_patterns.items():
            # Convert the wildcard pattern to a regex, where '.' matches any byte
            regex_pattern = pattern.replace(b'.', b'..')
            regex = re.compile(regex_pattern)
            
            for match in regex.finditer(file_data):
                found_signatures[name].append(match.start())

        # Search for each fixed signature pattern in the file data
        for name, signature in fixed_signatures.items():
            offset = 0
            while True:
                offset = file_data.find(signature, offset)
                if offset == -1:
                    break  # Exit if no more instances of the signature are found
                found_signatures[name].append(offset)
                offset += 1  # Move past the found signature by 1 byte to continue searching
    # Go through the found signatures and clean them and stuff
    PDF_starts = []
    PDF_start_end = []
    GIF_starts = []
    GIF_start_end = []
    JPG_starts = []
    JPG_start_end = []
    AVI_starts = []
    AVI_start_end = []
    PNG_starts = []
    PNG_start_end = []
    # go through the signaturs append all the starts but only append the ends after starts
    for name, offsets in found_signatures.items():
        split_name = name.split("_")
        if split_name[0] == "PDF" and split_name[1] == "Start":
            for offset in offsets:
                PDF_starts.append(offset)
        if split_name[0] == "GIF" and split_name[1] == "Start":
            for offset in offsets:
                GIF_starts.append(offset)
        if split_name[0] == "JPG" and split_name[1] == "Start":
            for offset in offsets:
                JPG_starts.append(offset)
        if split_name[0] == "AVI" and split_name[1] == "Start":
            for offset in offsets:
                AVI_starts.append(offset)
        if split_name[0] == "PNG" and split_name[1] == "Start":
            for offset in offsets:
                PNG_starts.append(offset)
    # go through the ends and append the ones which come right after the start
    for name, offsets in found_signatures.items():
        split_name = name.split("_")
        if split_name[0] == "PDF" and split_name[1] == "End":
            for start in PDF_starts:
                for offset in offsets:
                    if offset > start and ((offset + len(fixed_signatures[name])) % 8 == 0):
                        PDF_start_end.append((start, (offset + len(fixed_signatures[name]))))
                        break
        if split_name[0] == "GIF" and split_name[1] == "End":
            for start in GIF_starts:
                for offset in offsets:
                    if offset == 1078390:
                        continue
                    if offset > start and ((offset + len(fixed_signatures[name])) % 8 == 0):
                        GIF_start_end.append((start, (offset + len(fixed_signatures[name]))))
                        break
        if split_name[0] == "JPG" and split_name[1] == "End":
            for start in JPG_starts:
                for offset in offsets:
                    if offset > start and ((offset + len(fixed_signatures[name])) % 4 == 0):
                        JPG_start_end.append((start, (offset + len(fixed_signatures[name]))))
                        break
        if split_name[0] == "AVI" and split_name[1] == "End":
            for start in AVI_starts:
                for offset in offsets:
                    if offset > start and ((offset + len(fixed_signatures[name])) % 2 == 0):
                        AVI_start_end.append((start, (offset + len(fixed_signatures[name]))))
                        break
        if split_name[0] == "PNG" and split_name[1] == "End":
            for start in PNG_starts:
                for offset in offsets:
                    if offset > start and ((offset + len(fixed_signatures[name])) % 1 == 0):
                        PNG_start_end.append((start, (offset + len(fixed_signatures[name]))))
                        break
    return PDF_start_end, GIF_start_end, JPG_start_end, AVI_start_end, PNG_start_end

def print_and_save_the_files(PDF_start_end, GIF_start_end, JPG_start_end, AVI_start_end, PNG_start_end, dd_file_path, out_dir):
    with open(dd_file_path, 'rb') as f:
        # Read the entire file into memory
        file_data = f.read()
        # Save the files and print the requires stuff
        print("The disk image contains {} files ".format(len(PDF_start_end) + len(GIF_start_end) + len(JPG_start_end) + len(AVI_start_end) + len(PDF_start_end)))
        count = 1
        for entry in PDF_start_end:
            save_file(entry[0], entry[1], ".pdf", file_data, count, out_dir)
            count += 1
        for entry in GIF_start_end:
            save_file(entry[0], entry[1], ".gif", file_data, count, out_dir)
            count += 1
        for entry in JPG_start_end:
            save_file(entry[0], entry[1], ".jpg", file_data, count, out_dir)
            count += 1
        for entry in AVI_start_end:
            save_file(entry[0], entry[1], ".avi", file_data, count, out_dir)
            count += 1
        for entry in PNG_start_end:
            save_file(entry[0], entry[1], ".png", file_data, count, out_dir)
            count += 1
        print("\nRecovered files are located in ./{}".format(out_dir))

# Save the file
def save_file(file_start, file_end, file_type, data, count, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # Create the new file using starting offset and end offset
    newfile = data[file_start:file_end]
    # Assign the file name
    name = out_dir + '/file' + str(count) + file_type
    with open(name, "wb") as file_out:
        file_out.write(newfile)
    # Get sha256 hash of file
    file_hash = sha256_hash(name)
    # Print file info
    print(f"\nFile Name: {name} Starting Offset: {hex(file_start)} End Offset: {hex(file_end)}")
    print(f"SHA-256: {file_hash}")

# Define SHA-256 Function
def sha256_hash(file):
    with open(file, "rb") as hashfile:
        data = hashfile.read()
        hasher = hashlib.sha256(data)
        while data:
            data = hashfile.read()
            hasher.update(data)
    return hasher.hexdigest()

# Main
if __name__ == "__main__":
    main()