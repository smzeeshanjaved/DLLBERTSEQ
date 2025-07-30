import os
import csv
import pandas as pd
input_folder = r'E:\DatasetLabels\DLLVTLabels'
output_csv = 'DLLVTLabels.csv'

# Define only the AV engines you want to extract
selected_av_engines = {'AVG', 'Fortinet', 'Ikarus', 'Kaspersky', 'Microsoft'}
parsed_data = []

# Process each file
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            line = f.read().strip()
            if ':' not in line:
                continue

            hash_val, detections_str = line.split(':', 1)
            av_detections = detections_str.split(',')

            detection_map = {'hash': hash_val}

            for av_entry in av_detections:
                if '_' in av_entry:
                    av_name, label = av_entry.split('_', 1)
                    if av_name in selected_av_engines:
                        detection_map[av_name] = label
                else:
                    continue  # Skip entries without the expected format

            parsed_data.append(detection_map)

# Define fieldnames for CSV
fieldnames = ['hash'] + sorted(selected_av_engines)

# Write filtered data to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in parsed_data:
        writer.writerow(row)

print(f"Filtered CSV created: {output_csv}")

# Load the CSV file
df = pd.read_csv(output_csv)

# Directory to save split files
output_dir = 'Labelresult'
os.makedirs(output_dir, exist_ok=True)

# Get the list of AV engines (excluding 'hash')
av_engines = [col for col in df.columns if col.lower() != 'hash']

# Split and save individual files
for av in av_engines:
    sub_df = df[['hash', av]].dropna()  # Drop rows where AV label is missing
    output_path = os.path.join(output_dir, f'{av}.csv')
    sub_df.to_csv(output_path, index=False)

print(f"Successfully saved {len(av_engines)} CSV files to '{output_dir}' directory.")
