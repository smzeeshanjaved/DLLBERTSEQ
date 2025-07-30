import os
import json
import shutil
import pandas as pd
from tqdm import tqdm

extract_dir = r'E:\DatasetBehaviour\DLLSPBehaviour\C2AE'
labeled_csv_path = "DLLBERTSEQ.csv"

target_columns = [
    "filename_hash", "verdict_labels", "command_executions", "processes_tree",
    "http_conversations", "processes_terminated", "memory_pattern_urls",
    "registry_keys_set", "memory_pattern_domains", "registry_keys_deleted",
]

labeled_rows = []


def flatten_dict(d, prefix=""):
    flat = {}
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            flat.update(flatten_dict(v, new_key))
        elif isinstance(v, list):
            flat[new_key] = "; ".join(str(item) for item in v) if v else "[]"
        else:
            flat[new_key] = v
    return flat


# === Find JSON files ===
json_files = [
    os.path.join(root, filename)
    for root, _, files in os.walk(extract_dir)
    for filename in files if filename.endswith(".json")
]

# === Process JSON files ===
for file_path in tqdm(json_files, desc="Processing files", unit="file"):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error processing {filename}: {e}")
        continue

    attributes = data.get("attributes", {})
    flattened = flatten_dict(attributes)

    hash_value = os.path.splitext(filename)[0]

    # Build row, explicitly ensuring 'verdict_labels' is handled
    filtered_row = {col: flattened.get(col, "") for col in target_columns if col != "verdict_labels"}
    filtered_row["filename_hash"] = hash_value
    filtered_row["verdict_labels"] = flattened.get("verdict_labels", "")

    labeled_rows.append(filtered_row)

    # Handle verdicts (optional use-case, can be omitted if not copying files)
    verdicts = flattened.get("verdict_labels", "")
    if isinstance(verdicts, str):
        verdicts = [verdicts]
    elif isinstance(verdicts, list):
        pass
    else:
        verdicts = [str(verdicts)]

    for verdict in verdicts:
        safe_verdict = verdict.replace(" ", "_").replace("/", "_")
        # You can add logic here if you want to copy files based on verdicts

# === Build DataFrame ===
df = pd.DataFrame(labeled_rows, columns=target_columns)


# === Combine features for BERT input ===
def combine_features(row):
    parts = []
    if pd.notna(row["command_executions"]) and row["command_executions"]:
        parts.append(f"Commands: {row['command_executions']}")
    if pd.notna(row["processes_tree"]) and row["processes_tree"]:
        parts.append(f"Processes: {row['processes_tree']}")
    if pd.notna(row["http_conversations"]) and row["http_conversations"]:
        parts.append(f"HTTP: {row['http_conversations']}")
    if pd.notna(row["processes_terminated"]) and row["processes_terminated"]:
        parts.append(f"Terminated: {row['processes_terminated']}")
    if pd.notna(row["memory_pattern_urls"]) and row["memory_pattern_urls"]:
        parts.append(f"URLs: {row['memory_pattern_urls']}")
    if pd.notna(row["registry_keys_set"]) and row["registry_keys_set"]:
        parts.append(f"RegistrySet: {row['registry_keys_set']}")
    if pd.notna(row["memory_pattern_domains"]) and row["memory_pattern_domains"]:
        parts.append(f"Domains: {row['memory_pattern_domains']}")
    if pd.notna(row["registry_keys_deleted"]) and row["registry_keys_deleted"]:
        parts.append(f"RegistryDeleted: {row['registry_keys_deleted']}")
    return " ".join(parts).strip()


# Apply to create BERT input
df["bert_input"] = df.apply(combine_features, axis=1)

# Drop rows with empty BERT input
df = df[df["bert_input"] != ""]

# Save to CSV
df[["filename_hash", "bert_input", "verdict_labels"]].to_csv(labeled_csv_path, index=False)
print(f" Labeled BERT data saved to: {labeled_csv_path}")
