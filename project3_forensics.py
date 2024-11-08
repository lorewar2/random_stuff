#!/usr/bin/env python3
import hashlib  # used for SHA256

def main():
    filename = "project3.dd"
    # Define Header signatures
    header_markers = [
        b'\x00\x00\x01\xB3', # MPG
        b'\x00\x00\x01\xBA', # MPG
        b'\x25\x50\x44\x46', # pdf
        b'\x47\x49\x46\x38\x37\x61', # GIF
        b'\x47\x49\x46\x38\x39\x61', # GIF
        b'\xFF\xD8\xFF\xE0', # JPG
        b'\xFF\xD8\xFF\xE1', # JPG
        b'\xFF\xD8\xFF\xE2', # JPG
        b'\xFF\xD8\xFF\xE8', # JPG
        b'\xFF\xD8\xFF\xDB', # JPG
        b'\x50\x4B\x03\x04\x14\x00\x06\x00', # DOCX
        b'\x50\x4B\x05\x06', # ZIP
        b'\x52\x49\x46\x46', # AVI
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A' # PNG
    ]
    # Define footer signatures
    footer_markers = [
        b'\x00\x00\x01\xB7', # MPG
        b'\x00\x00\x01\xB9', # MPG
        b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A', # PDF
        b'\x0A\x25\x25\x45\x4F\x46\x0A', # PDF
    ]
    header_marker_start_list, footer_marker_end_list = extract_header_footer(find_header_footer_offsets, filename, header_markers, footer_markers)
    # Initialize file count
    count = 1
    # Disk image variable
    with open(filename, 'rb') as file:
        data = file.read()
    # Save the mpgs # needs modification
    with open(filename, 'rb') as file:
        data = file.read()
        # mpg file header at index 0
        start = header_marker_start_list[0][1]
        end = footer_marker_end_list[0][1] + 4 #added 4 as the size of the footer signature
        #save the mpg file
        save_file(start, end, '.mpg', data)

# Appending Header and footer into the list as per file type
def extract_header_footer(find_header_footer_offsets, filename, header_markers, footer_markers):
    # Run the header and footer function
    header_offsets, footer_offsets = find_header_footer_offsets(filename, header_markers, footer_markers)
    header_marker_start_list = []
    # Verify each header offset
    for header_marker, offsets in header_offsets.items():
        for offset in offsets:
            # Bytes per sector=512 and sector per cluster=8 so, cluster size is 4096
            # When offset is divided by 4096 and remainder is 0, we consider that offset as a valid offset
            if offset % 4096 == 0:
                start = offset
                # Append Header offset and header marker into a single list
                header_marker_start_list.append((header_marker, start))
            else:
                start = 0

    # Append footer offset and footer marker into a single list
    footer_marker_end_list = []
    for footer_marker, offsets in footer_offsets.items():
        for offset in offsets:
            # If offset is not zero
            if offset != 0:
                start = offset
                # Append Footer offset and footer marker into a single list
                footer_marker_end_list.append((footer_marker, start))
            else:
                start = 0

    # Combine header and footer offset into a single list
    combined_list = list(zip(header_marker_start_list, footer_marker_end_list))
    output_list = []
    # Match the header and footer as per file type
    for row in combined_list:
        output_list.append(row)
    return header_marker_start_list, footer_marker_end_list

# Define SHA-256 Function
def sha256_hash(file):
    with open(file, "rb") as hashfile:
        data = hashfile.read()
        hasher = hashlib.sha256(data)
        while data:
            data = hashfile.read()
            hasher.update(data)
    return hasher.hexdigest()

# Define Header and Footer offset function
def find_header_footer_offsets(filename, header_markers, footer_markers):
    header_offsets = {}
    footer_offsets = {}
    with open(filename, 'rb') as file:
        data = file.read()

        # Match each header file signatures in disk image
        for header_marker in header_markers:
            header_offsets[header_marker] = []
            # Find the header offset in the disk image
            header_index = data.find(header_marker)
            # If header offset is identified
            while header_index != -1:
                # Add header offset list
                header_offsets[header_marker].append(header_index)
                header_index = data.find(header_marker, header_index + 1)

        # Match each footer file signatures in disk image
        for footer_marker in footer_markers:
            footer_offsets[footer_marker] = []
            # Find the footer offset in the disk image
            footer_index = data.rfind(footer_marker)
            # If footer offset is identified
            while footer_index != -1:
                # Add footer offset to the list
                footer_offsets[footer_marker].append(footer_index)
                footer_index = data.find(footer_marker, footer_index + 1)

    return header_offsets, footer_offsets

# Save the file
def save_file(file_start, file_end, file_type, data):
    # Count the number of files
    global count
    # Create the new file using starting offset and end offset
    newfile = data[file_start:file_end]
    # Assign the file name
    name = 'file' + str(count) + file_type
    with open(name, "wb") as file_out:
        file_out.write(newfile)
    # Get sha256 hash of file
    file_hash = sha256_hash(name)
    # Increment file counter
    count += 1
    # Print file info
    print(f"\nFile Name: {name}")
    print(f"Starting Offset: {hex(file_start)}")
    print(f"End Offset: {hex(file_end)}")
    print(f"SHA-256 Hash: {file_hash}")

# Main
if __name__ == "__main__":
    main()