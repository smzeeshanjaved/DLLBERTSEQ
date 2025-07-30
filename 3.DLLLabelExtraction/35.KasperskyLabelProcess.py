import csv

def clean_label(label):
    return label.replace("HEUR:", "").replace("UDS:", "")

with open('Labelresult/kaspersky.csv', 'r') as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# Clean the labels (skip header if present)
header = data[0]
rows = data[1:]
cleaned_rows = [[row[0], clean_label(row[1])] for row in rows]

# Write output
with open('cleaned_kaspersky.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(cleaned_rows)

def simplify_kaspersky_label(label):
    """
    Extract the family name from a Kaspersky label.
    Typically, it's the second last component, e.g.,
    'Trojan-Downloader.Win32.Convagent.gen' → 'Convagent'
    """
    parts = label.split('.')
    return parts[-2] if len(parts) >= 2 else label


def process_kaspersky_file(input_file, output_file):
    """
    Process the input CSV to extract simplified labels and save to output CSV.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read and write header
        header = next(reader)
        writer.writerow(header)

        # Process each row
        for row in reader:
            if len(row) == 2:
                hash_value = row[0]
                original_label = row[1]
                simplified_label = simplify_kaspersky_label(original_label)
                writer.writerow([hash_value, simplified_label])


if __name__ == "__main__":
    input_filename = "cleaned_kaspersky.csv"
    output_filename = "simplified_kaspersky.csv"

    process_kaspersky_file(input_filename, output_filename)
    print(f"Simplified labels written to {output_filename}")

import csv
from collections import Counter
import matplotlib.pyplot as plt


def plot_top_10_labels(csv_file):
    # Read the simplified labels
    labels = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                labels.append(row[1])

    # Count label occurrences
    label_counts = Counter(labels)
    top_10 = label_counts.most_common(15)

    # Prepare data for plotting
    categories = [item[0] for item in top_10]
    counts = [item[1] for item in top_10]

    # Create the plot
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, counts, color='skyblue')

    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height}',
                 ha='center', va='bottom')

    # Customize the plot
    plt.title('Top 10 Malware Categories (Simplified Kaspersky Labels)')
    plt.xlabel('Malware Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save and show the plot
    plt.savefig('top_10_malware_categories.png')
    plt.show()
    # Print the top 10 counts
    print("Top 10 Threat Categories:")
    for category, count in top_10:
        print(f"{category}: {count}")


if __name__ == "__main__":
    input_file = "simplified_kaspersky.csv"
    plot_top_10_labels(input_file)

