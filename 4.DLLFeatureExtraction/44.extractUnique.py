import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('DLLBERTSEQ.csv')
print("Data Head:\n", data.head())
print("Data Info:\n", data.info())
label_counts = data['verdict_labels'].value_counts()
top_30_labels = label_counts.head(30)
print("Top 30 unique labels and their counts:")
print(top_30_labels)
metrics_df = pd.DataFrame({
    "Label": top_30_labels.index,
    "Count": top_30_labels.values
})
cmap = plt.get_cmap("tab10")
colors = [cmap(i % 10) for i in range(len(metrics_df))]  # Cycle through tab10 colors
plt.figure(figsize=(14, 8))
bars = plt.bar(metrics_df["Label"], metrics_df["Count"], color=colors)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             str(bar.get_height()), ha='center', va='bottom', fontsize=10, fontweight='bold')
total_count = label_counts.sum()
plt.title(f" Label Distribution (Total: {total_count})", fontsize=16)
plt.xlabel("Labels")
plt.ylabel("Count")
plt.xticks(rotation=90, ha="right")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("OFF_BERT_input25740.png", dpi=300, bbox_inches="tight")
plt.show()


