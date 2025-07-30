import pandas as pd

# Load the CSV file
data = pd.read_csv('DLL_BERT.csv')

data['verdict_labels'] = data['verdict_labels'].str.replace('Cridex', 'Dridex')

# Drop rows where 'verdict_labels' is NaN
data = data.dropna(subset=['verdict_labels'])

# Remove specific unwanted mixed labels
data = data.dropna(subset=['verdict_labels'])

# Split labels, count occurrences
label_counts = (
    data['verdict_labels']
    .str.split(';')
    .explode()
    .str.strip()
    .value_counts()
)

# Define a frequency threshold
frequency_threshold = 4000

# Identify labels to keep
labels_to_keep = set(label_counts[label_counts >= frequency_threshold].index)

# Remove infrequent labels from each row
data['verdict_labels'] = data['verdict_labels'].apply(
    lambda x: ';'.join([label.strip() for label in x.split(';') if label.strip() in labels_to_keep])
)

# Drop rows that have no labels left after filtering
filtered_data = data[data['verdict_labels'] != '']

# Save the filtered data
filtered_data.to_csv('DLLBERTSEQ.csv', index=False)

# Print dataset shape and label counts
print(f"Filtered dataset shape: {filtered_data.shape}")
print("Unique labels and their counts:")
print(label_counts[label_counts >= frequency_threshold])
