#441737
import json
import os
import re
import shutil  # Import shutil for moving files
from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
def save_behavior(directory, filename, behavior_data):
    """Saves behavior data to the specified directory and file."""
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, "w") as file:
        json.dump(behavior_data, file, indent=4)
def extract_and_log_sandbox_data(input_dir, output_dir, log_file, processed_dir):
    """
    Extracts sandbox data from JSON files, saves it in categorized directories,
    and logs sandbox details into a file, with progress tracking.
    After processing, moves files to `processedEXEVTBehaviour`.
    """
    #os.makedirs(processed_dir, exist_ok=True)  # Ensure processed folder exists
    sandbox_dirs = {}
    json_files = list(filter(lambda f: f.endswith(".json"), os.listdir(input_dir)))

    with open(log_file, "w") as log:
        for filename in tqdm(json_files, desc="Processing JSON files"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)

                sandbox_names = [
                    item.get("attributes", {}).get("sandbox_name", "Unknown")
                    for item in data.get("data", [])
                ]
                sandbox_counts = Counter(sandbox_names)

                # Log sandbox details
                log.write(f"{filename}:\n")
                log.write(f"  Total sandboxes: {len(sandbox_names)}\n")
                log.write("  Sandbox details:\n")
                for sandbox_name, count in sandbox_counts.items():
                    log.write(f"    {sandbox_name}: {count}\n")
                log.write("\n")

                # Save behavior data
                for item in data.get("data", []):
                    sandbox_name = item.get("attributes", {}).get("sandbox_name", "Unknown")
                    sanitized_name = re.sub(r'\W+', '_', sandbox_name)
                    sandbox_dir = sandbox_dirs.setdefault(
                        sanitized_name, os.path.join(output_dir, sanitized_name)
                    )
                    save_behavior(sandbox_dir, filename, item)

                # Move processed file to processed directory
                #shutil.move(file_path, os.path.join(processed_dir, filename))

            except (json.JSONDecodeError, KeyError) as e:
                log.write(f"Error processing {filename}: {e}\n")
            except Exception as e:
                log.write(f"Unexpected error in {filename}: {str(e)}\n")

def get_class_file_counts(directory):
    """Counts the number of files in each class directory."""
    return {
        class_name: len([f for f in os.listdir(os.path.join(directory, class_name))
                         if os.path.isfile(os.path.join(directory, class_name, f))])
        for class_name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, class_name))
    }

def plot_architecture_bar_chart(file_type_counts, output_file, total_count, sandbox_name, n):
    """Plots a bar chart of file types with counts displayed on the bars and total count in the title."""
    top_n_file_types = sorted(file_type_counts, key=lambda x: x[1], reverse=True)[:n]
    labels, counts = zip(*top_n_file_types)

    df = pd.DataFrame(top_n_file_types, columns=['Malware Sample Type', 'Malware Sample Count'])

    sns.set(style="whitegrid")

    for palette in ['viridis', 'Blues_d', 'deep', 'muted', 'pastel', 'Set1']:
        plt.figure(figsize=(12, 6))
        barplot = sns.barplot(x='Malware Sample Type', y='Malware Sample Count', data=df, palette=palette)

        for p in barplot.patches:
            barplot.annotate(format(p.get_height(), '.0f'),
                             (p.get_x() + p.get_width() / 2., p.get_height()),
                             ha='center', va='center',
                             fontsize=10, color='black',
                             xytext=(0, 9), textcoords='offset points')

        plt.xlabel("Malware Sample Type", fontweight="bold")
        plt.ylabel("Malware Sample Count", fontweight="bold")
        plt.title(f"Malware Distribution According to {sandbox_name} Sandbox ({total_count} Malware Samples)",
                  fontweight="bold")

        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.tight_layout()
        output_filename = f"Charts\\{output_file}_{palette}.png"

        plt.savefig(output_filename)
        plt.close()

        print(f"Bar chart saved as {output_filename}")

# Main Script
if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Script started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    input_dir = r'D:\Dataset\ELFVTBehaviour'
    parent_output_dir = "D:\Dataset\IOTSPBehaviour"
    processed_dir = "D:\Dataset\IOTVTBehaviour"
    log_file = "sandbox_details.txt"

    extract_and_log_sandbox_data(input_dir, parent_output_dir, log_file, processed_dir)

    class_counts = get_class_file_counts(parent_output_dir)
    plot_architecture_bar_chart(class_counts.items(), 'SandBox_bar_chart', sum(class_counts.values()), 'IOT', 20)


    end_time = datetime.now()
    print(f"Script ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {end_time - start_time}")
