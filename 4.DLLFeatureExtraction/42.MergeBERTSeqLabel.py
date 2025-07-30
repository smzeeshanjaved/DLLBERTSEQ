import pandas as pd

# Load both CSV files
df_droidy = pd.read_csv("DLLBERTSEQ.csv")  # Contains: filename_hash, bert_input, verdict_labels
df_kaspersky = pd.read_csv("simplified_kaspersky.csv")  # Contains: hash, Kaspersky

# Rename columns for consistent merging
df_droidy = df_droidy.rename(columns={"filename_hash": "hash"})
df_kaspersky = df_kaspersky.rename(columns={"Kaspersky": "kaspersky_label"})

# Merge Kaspersky verdicts into Droidy data on 'hash'
merged_df = pd.merge(df_droidy, df_kaspersky, on='hash', how='left')

# Update Droidy's verdict_labels with Kaspersky's label where available
merged_df['verdict_labels'] = merged_df['kaspersky_label'].combine_first(merged_df['verdict_labels'])

# Drop temporary Kaspersky column
merged_df.drop(columns=['kaspersky_label'], inplace=True)

# Save the updated CSV
merged_df.to_csv("DLL_BERT.csv", index=False)

# Optional: print stats
updated_count = merged_df['hash'].isin(df_kaspersky['hash']).sum()
print(f"Updated verdict_labels for {updated_count} hashes from Kaspersky.")
