# Number of entries: 967815
import os
import requests
import pyzipper

API_URL = "https://mb-api.abuse.ch/api/v1/"
API_KEY = "2dd3cdd1b4c736d3eafe69a54faf90c442064be1b22395d7"
PASSWORD = b'infected'

save_dir = r"E:/MalwareBazaarDownload"
os.makedirs(save_dir, exist_ok=True)

headers = {"Auth-Key": API_KEY}

# Read hashes from result.txt
with open("result.txt", "r") as f:
    hashes = [line.strip() for line in f if line.strip()]

for sha256 in hashes:
    file_path = os.path.join(save_dir, f"{sha256}.zip")
    data = {"query": "get_file", "sha256_hash": sha256}

    print(f"\n[*] Downloading sample for hash: {sha256}")

    try:
        response = requests.post(API_URL, headers=headers, data=data)

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)

            try:
                with pyzipper.AESZipFile(file_path) as zf:
                    zf.pwd = PASSWORD
                    zf.extractall(save_dir)
                    print(f"[+] Sample `{sha256}` downloaded and extracted to {save_dir}")

                # Remove the zip after successful extraction
                os.remove(file_path)
                print(f"[+] Removed archive: {file_path}")

            except pyzipper.zipfile.BadZipFile:
                print(f"[!] Error: {file_path} is not a valid ZIP file.")
        else:
            print(f"[!] Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[!] Exception for {sha256}: {e}")
