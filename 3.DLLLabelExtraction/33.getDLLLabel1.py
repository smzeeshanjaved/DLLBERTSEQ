import json
import os
import time
import requests

# List of VirusTotal API keys
vt_api_keys = [
        "1cd176f0b34a171b45a15e34ff211a9f1ca2abfb77c28e133838f7adfac2e8eb",
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
    "d7fe4e800073c5c6cd910f72ae76506a1e659330960e6e82d3ebfbc00250e119",
    "20e0b632418c43c902561eb366f4fb767fd78496b89dabe0e02386db0747f6df",
    "21b2774c74d026d9cc33db6a2ffacc5a8885e2c199493bf705432bfb0fb8090f",
    "9ed3b5fcc8d3a112b586db665ab6be740b6759d465dc72d246e608ea789ca57a",
    "547949d9d3662c5094ec68e72fc88a902ed537f371cbbc70dafac2d112219f51",
    "e440db8d8d51763de5ce4fa426b5b1d82a38f6f98aa9a70072bf45f8caa71f98",
    "d856f94772878ae4dbc6984ea6d6f9e34d93fde09b6a019cb681f50f04d6084a",
    "95051aa2035a1bde2ced33911efd22dade939b83649d9cb1e8605a0382a5c6b0",
    "be947fe6ad97dd6d96d41ec946618338454425adaabdb59017c0362dc26c7e49",
    "253311ee35173a3ca769d08e37c14d434dade112522b3f12d0e74040320eed65",
    "3c95a0858c856e879413d4aa326694fb26b7217539a7f6c285ad975c1e3a43d1",
]

def report_virus(resource, api_key):
    params = {'apikey': api_key, 'resource': resource}
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "gzip, My Python requests library example client"
    }
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
                            params=params, headers=headers)
    return response

def ask_to_virus_total_service(resource, api_key):
    try:
        return report_virus(resource, api_key)
    except Exception as e:
        print("ask_to_virus_total_service..." + str(e))
        return ask_to_virus_total_service(resource, api_key)

def fetch_engine_values(resource, api_key, retries=3, delay=10):
    for attempt in range(retries):
        response = ask_to_virus_total_service(resource, api_key)

        if response.status_code == 200:
            json_response = response.json()
            scans = json_response.get("scans")
            if scans is None:
                return f"{resource}:No scans data"
            result_str = resource + ":"
            for engine, engine_info in scans.items():
                if engine_info.get("detected") is True:
                    result = engine_info.get("result", "malicious")
                    result_str += f"{engine}_{result},"
            return result_str

        elif response.status_code == 204:
            print(f"HTTP 204 No Content for {resource}, retrying {attempt + 1}/{retries} after {delay}s...")
            time.sleep(delay)
            continue
        else:
            return f"{resource}:Error_HTTP_{response.status_code}"

    return f"{resource}:Error_HTTP_204_After_{retries}_Retries"

# Initialize the API key index
vt_api_key_index = 0

# Directory where all results will be saved
output_dir = r'E:\DatasetLabels\DLLVTLabels'

os.makedirs(output_dir, exist_ok=True)

hash_file_path = "remain1.txt"
with open(hash_file_path, "r") as file:
    index = 0
    for line in file:
        index += 1
        hash_value = line.strip()
        vt_api_key = vt_api_keys[vt_api_key_index]
        print(f"[{index}] Requesting for hash {hash_value} using API key {vt_api_key[:8]}...")

        try:
            scan_result = fetch_engine_values(hash_value, vt_api_key)
            if "Error_HTTP_204" in scan_result:
                # Skip saving and continue to next hash
                print(f"{hash_value}: No content, skipping save.")
                vt_api_key_index = (vt_api_key_index + 1) % len(vt_api_keys)
                continue

            print(scan_result)

            # Save only if there is meaningful scan result
            output_file_path = os.path.join(output_dir, f"{hash_value}")
            with open(output_file_path, "w") as f_out:
                f_out.write(scan_result + "\n")

        except Exception as e:
            print(f"Error fetching behaviour for hash {hash_value}: {e}")

        vt_api_key_index = (vt_api_key_index + 1) % len(vt_api_keys)
        # time.sleep(4)  # Optional delay

