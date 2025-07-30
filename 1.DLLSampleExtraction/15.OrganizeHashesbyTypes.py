# Number of entries: 920613 Final
import os
def get_file_names(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
def group_files_by_extension(file_names):
    grouped_files = {}
    for file_name in file_names:
        ext = file_name.split('.')[-1]  # Extract the file extension
        if ext not in grouped_files:
            grouped_files[ext] = []
        grouped_files[ext].append(file_name)
    return grouped_files
# Replace 'your_directory_path' with the path to your directory
directory_path =  r'D:\MalwareBazaarDownload'
# Get all file names in the specified directory
file_names = get_file_names(directory_path)
# Group files by their extension
grouped_files = group_files_by_extension(file_names)

# Define the base path for the output files
output_directory = 'Downloaded_files_by_type/'

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Process each group of files by extension and save their names
for ext, files in grouped_files.items():
    # Define output file path for the current extension's file names
    output_file_path = os.path.join(output_directory, f'{ext}_files.txt')

    # Write the file names for the current extension to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for file_name in files:
            print(f'Processed file: {file_name}')  # Optional: Print file name to the console
            file_name = os.path.splitext(file_name)[0]
            output_file.write(f'{file_name}\n')
            print(f'Processed file: {file_name}')  # Optional: Print file name to the console

    print(f"File names for {len(files)} '{ext}' files have been written to '{output_file_path}'.")

print("File grouping complete for all file types.")
