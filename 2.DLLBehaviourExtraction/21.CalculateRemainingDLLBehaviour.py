import os
def get_file_names(directory_path):
    """Retrieve the names of all files in the specified directory."""
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
# Replace 'your_directory_path' with the path to your directory
directory_path = r'D:\MalwareBazaarDownloads\DLL'
# Get all file names in the specified directory
file_names = get_file_names(directory_path)
# Define the output file path for the hashes
output_file_path = 'dll_files'
# Save all file names into the single output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for file_name in file_names:
        output_file.write(file_name + '\n')
print(f"Extracted {len(file_names)} hashes into '{output_file_path}'.")
# Specify the input and output file paths
input_file = 'dll_files'
output_file = 'dll_files.txt'
# Read hashes from the input file
with open(input_file, 'r', encoding='utf-8') as infile:
    hashes = infile.readlines()
# Clean the hashes (remove all extensions and surrounding whitespace)
cleaned_hashes = [os.path.splitext(hash.strip())[0] for hash in hashes]
# Write the cleaned hashes to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for hash in cleaned_hashes:
        outfile.write(hash + '\n')
print(f"Cleaned {len(cleaned_hashes)} hashes written to '{output_file}'.")


# Replace 'your_directory_path' with the path to your directory
directory_path =r'D:\Dataset\DLLVTBehaviour'
# Get all file names in the specified directory
file_names = get_file_names(directory_path)
# Define the output file path for the hashes
output_file_path = 'dllBehaviour'
# Save all file names into the single output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for file_name in file_names:
        output_file.write(file_name + '\n')
print(f"Extracted {len(file_names)} hashes into '{output_file_path}'.")
# Specify the input and output file paths
input_file = 'dllBehaviour'
output_file = 'dllBehaviour.txt'
# Read hashes from the input file
with open(input_file, 'r', encoding='utf-8') as infile:
    hashes = infile.readlines()
# Clean the hashes (remove all extensions and surrounding whitespace)
cleaned_hashes = [os.path.splitext(hash.strip())[0] for hash in hashes]
# Write the cleaned hashes to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for hash in cleaned_hashes:
        outfile.write(hash + '\n')
print(f"Cleaned {len(cleaned_hashes)} hashes written to '{output_file}'.")




def read_hashes(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file if line.strip())
# Main function
def find_unique_hashes():
    remaining_file = 'dll_files.txt'
    total_file = 'dllBehaviour.txt'
    output_file = 'remain.txt'
    # Load hashes from both files
    remaining_hashes = read_hashes(remaining_file)
    total_hashes = read_hashes(total_file)

    # Find hashes in remaining.txt but not in total.txt
    unique_hashes = remaining_hashes - total_hashes
    # Write the unique hashes to the output file
    with open(output_file, 'w') as file:
        for hash_value in sorted(unique_hashes):  # Sorting is optional
            file.write(f"{hash_value}\n")

    print(f"Unique hashes written to {output_file}. Total: {len(unique_hashes)}")



def split_hashes(input_file, output_file1, output_file2):
    # Read all lines (hashes) from the input file
    with open(input_file, "r") as file:
        hashes = file.readlines()
    # Determine the midpoint
    midpoint = len(hashes) // 2
    # Split into two parts
    hashes_part1 = hashes[:midpoint]
    hashes_part2 = hashes[midpoint:]
    # Save each part into separate files
    with open(output_file1, "w") as file1:
        file1.writelines(hashes_part1)

    with open(output_file2, "w") as file2:
        file2.writelines(hashes_part2)

    print(f"Split complete.\nFirst half saved to: {output_file1}\nSecond half saved to: {output_file2}")



# Execute the function
if __name__ == "__main__":
    find_unique_hashes()
    input_file = "remain.txt"
    output_file1 = "remain.txt"  # Overwrites original with first half
    output_file2 = "remain1.txt"  # Second half goes here
    split_hashes(input_file, output_file1, output_file2)
