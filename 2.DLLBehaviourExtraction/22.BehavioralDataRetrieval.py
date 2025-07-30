#152001
import json
import os
import time
import requests

# List of VirusTotal API keys
vt_api_keys = [
    "20e0b632418c43c902561eb366f4fb767fd78496b89dabe0e02386db0747f6df",
    "21b2774c74d026d9cc33db6a2ffacc5a8885e2c199493bf705432bfb0fb8090f",
    "9ed3b5fcc8d3a112b586db665ab6be740b6759d465dc72d246e608ea789ca57a",
    "547949d9d3662c5094ec68e72fc88a902ed537f371cbbc70dafac2d112219f51",
    "d856f94772878ae4dbc6984ea6d6f9e34d93fde09b6a019cb681f50f04d6084a",
    "95051aa2035a1bde2ced33911efd22dade939b83649d9cb1e8605a0382a5c6b0",
    "be947fe6ad97dd6d96d41ec946618338454425adaabdb59017c0362dc26c7e49",
    "253311ee35173a3ca769d08e37c14d434dade112522b3f12d0e74040320eed65",
    "3c95a0858c856e879413d4aa326694fb26b7217539a7f6c285ad975c1e3a43d1",
    "a004f1dfac74b7f2b7ef213b651f9443127902a8fc2ef3a4ce9c2a7b7c554908",
    "fd42686f70085351b7f052a6ac9129eb6bb754e9c9587cc1e609fd6264fa2ed4",
    "09cf0e09e702feda46fd29f46232564a1ca724e878f527a57953a4ab535e6050",
    "e440db8d8d51763de5ce4fa426b5b1d82a38f6f98aa9a70072bf45f8caa71f98",
    "9836c6bb69ff849ab3b7c3e285b5621c43352c7d64bbf863ae4ff173250810ba",
    "90449dfae0ad3ec9cf2ea74b2e6eb64c5fafb3bda01a090170e177e6d786b532",
    "55ffc55e4f0331dba29c44f796947e7e1ba5133f901fccfe75272da0c62cc91d",
    "d46a87c27a0e0c6bfc5c4afdd3216ba32216dcd2b41e3a36653fac48c8c0138b",
    "89790b917cf30ecc634a69a6865ac2afbd8f8bd80c917e7f05dc429546dc2e27",
    "8fb8fe5c2e63104b3a2be19c36c0d5b9bd9ba9c6ca5a3f82aab02f51d268e368",
    "59405c0d3bba4c019f670f041054d33ecaaad16ab5f3f8d68df45792dd78c514",
    "9c4ac2b1931430350e1b58a3dfe2a3de1d79847c6f2984f12ea303415ce21863",
    "2855913ff47320bed9382e9566bc27bcb42728a7342e43b613bb56b972fe0524",
    "d7fe4e800073c5c6cd910f72ae76506a1e659330960e6e82d3ebfbc00250e119"
]
# Initialize the API key index
vt_api_key_index = 0

# Directory where all JSON responses will be saved
output_dir = r'D:\Dataset\DLLVTBehaviour'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Open the single hash file
hash_file_path = "remain.txt"  # Change to the path of your single hash file
with open(hash_file_path, "r") as file:
    index = 0  # To keep track of the line number
    for line in file:
        index += 1
        hash_value = line.strip()  # Get the hash from the line

        # Select the appropriate VirusTotal API key
        vt_api_key = vt_api_keys[vt_api_key_index]

        # VirusTotal API URL for file behaviours
        virTotal3 = "https://www.virustotal.com/api/v3/files/"
        reqObject = "/behaviours"
        strLimit = "?limit=40"
        URL = virTotal3 + hash_value + reqObject + strLimit

        # Set the headers for the request
        headers = {
            "Accept": "application/json",
            "x-apikey": vt_api_key
        }

        print(f"Requesting for hash {hash_value} with API key {vt_api_key}...")

        # Send the request to VirusTotal API
        try:
            behavResponse = requests.get(URL, headers=headers)
            if behavResponse.status_code == 200:  # Check if the request is successful
                print(f"{time.strftime('%H:%M:%S')}: {index}: {vt_api_key}: {hash_value}")

                # Save the response to a file in the single output directory
                output_file_path = os.path.join(output_dir, f"{hash_value}.json")

                with open(output_file_path, 'w') as fp:
                    json.dump(behavResponse.json(), fp)
            else:
                print(f"Error for hash {hash_value}: {behavResponse.status_code}")

        except Exception as e:
            print(f"Error fetching behaviour for hash {hash_value}: {e}")

        # Rotate API keys
        vt_api_key_index = (vt_api_key_index + 1) % len(vt_api_keys)

        # Add a delay between requests to avoid rate limiting
