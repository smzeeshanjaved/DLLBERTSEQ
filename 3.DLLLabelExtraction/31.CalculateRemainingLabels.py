import os


def get_file_names(directory_path):
    """
    Extracts and returns the names of all files present in the specified directory.

    Parameters:
    directory_path (str): The absolute path to the target directory.

    Returns:
    list: A list containing file names from the directory.
    """
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]


# Define the directory containing labeled DLL samples
directory_path = r'E:\DatasetLabels\DLLVTLabels'

# Retrieve all filenames in the specified directory
file_names = get_file_names(directory_path)

# Save raw file names (assumed to be hash identifiers) into a text file
raw_output_path = 'DLLVTLabels'
with open(raw_output_path, 'w', encoding='utf-8') as output_file:
    for file_name in file_names:
        output_file.write(file_name + '\n')

print(f"Extracted {len(file_names)} hashes into '{raw_output_path}'.")

# Normalize filenames by removing extensions and storing them in a cleaned output file
cleaned_output_path = 'DLLVTLabels.txt'
with open(raw_output_path, 'r', encoding='utf-8') as infile:
    hashes = infile.readlines()

# Remove file extensions and whitespace
cleaned_hashes = [os.path.splitext(hash.strip())[0] for hash in hashes]

# Write cleaned hash values to a new file
with open(cleaned_output_path, 'w', encoding='utf-8') as outfile:
    for hash in cleaned_hashes:
        outfile.write(hash + '\n')

print(f"Cleaned {len(cleaned_hashes)} hashes written to '{cleaned_output_path}'.")

# Define file paths for hash comparison
remaining_file = 'dll_files.txt'  # Contains hashes from previously downloaded DLLs
total_file = 'DLLVTLabels.txt'  # Contains hashes of labeled DLL samples
output_file = 'remain.txt'  # Stores hashes that are not yet labeled


def read_hashes(file_path):
    """
    Reads and returns a set of non-empty, stripped hash strings from a file.

    Parameters:
    file_path (str): Path to the file containing hash entries.

    Returns:
    set: A set of unique hashes.
    """
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file if line.strip())


def find_unique_hashes():
    """
    Identifies and records the set of hashes present in the `remaining_file`
    but absent from the `total_file`, signifying unlabeled samples.
    """
    remaining_hashes = read_hashes(remaining_file)
    total_hashes = read_hashes(total_file)

    # Compute set difference to identify unlabeled hashes
    unique_hashes = remaining_hashes - total_hashes

    # Write resulting unique hashes to the output file
    with open(output_file, 'w') as file:
        for hash_value in sorted(unique_hashes):
            file.write(f"{hash_value}\n")

    print(f"Unique hashes written to '{output_file}'. Total: {len(unique_hashes)}")


def split_hashes(input_file, output_file1, output_file2):
    """
    Splits a list of hashes into two equal parts and saves each part into a separate file.

    Parameters:
    input_file (str): File containing the full set of hashes.
    output_file1 (str): File to store the first half of hashes.
    output_file2 (str): File to store the second half of hashes.
    """
    with open(input_file, "r") as file:
        hashes = file.readlines()

    midpoint = len(hashes) // 2
    hashes_part1 = hashes[:midpoint]
    hashes_part2 = hashes[midpoint:]

    with open(output_file1, "w") as file1:
        file1.writelines(hashes_part1)

    with open(output_file2, "w") as file2:
        file2.writelines(hashes_part2)

    print(f"Split complete.\nFirst half saved to: {output_file1}\nSecond half saved to: {output_file2}")


# Execute the primary workflow if the script is run as the main module
if __name__ == "__main__":
    find_unique_hashes()

    # Split the list of remaining hashes into two parts for further processing
    input_file = "remain.txt"
    output_file1 = "remain.txt"  # Overwrites with the first half
    output_file2 = "remain1.txt"  # Stores the second half
    split_hashes(input_file, output_file1, output_file2)
