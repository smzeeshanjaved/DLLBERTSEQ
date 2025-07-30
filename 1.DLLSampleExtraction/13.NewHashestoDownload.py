# Number of entries: 920613 Final
remaining_file = 'full_sha256.txt'
total_file = 'DownloadedHashes.txt'
output_file = 'result.txt'
def read_hashes(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file if line.strip())
# Main function
def find_unique_hashes():
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

# Execute the function
if __name__ == "__main__":
    find_unique_hashes()
