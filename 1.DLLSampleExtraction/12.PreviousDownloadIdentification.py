# Number of entries: 920613 Final
import os
def get_file_names(directory_path):
    """Retrieve the names of all files in the specified directory."""
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
# Replace 'your_directory_path' with the path to your directory
directory_path = r'D:\MalwareBazaarDownload'
# Get all file names in the specified directory
file_names = get_file_names(directory_path)
# Define the output file path for the hashes
output_file_path = 'DownloadedHashes'
# Save all file names into the single output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for file_name in file_names:
        output_file.write(file_name + '\n')
print(f"Extracted {len(file_names)} hashes into '{output_file_path}'.")
# Specify the input and output file paths
input_file = 'DownloadedHashes'
output_file = 'DownloadedHashes.txt'
# Read hashes from the input file
with open(input_file, 'r', encoding='utf-8') as infile:
    hashes = infile.readlines()

# Clean the hashes (remove all extensions and surrounding whitespace)
cleaned_hashes = [os.path.splitext(hash.strip())[0] for hash in hashes]

# Write the cleaned hashes to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for hash in cleaned_hashes:
        outfile.write(hash + '\n')

print(f"Cleaned hashes written to '{output_file}'.")
