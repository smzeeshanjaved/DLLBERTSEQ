# Number of entries: 920613 Final
import time
import requests
import pyzipper
import os
from concurrent.futures import ThreadPoolExecutor
PASSWORD = b'infected'
headers = {'API-KEY': '89ce6ff37f785312974a6dc8491290dc'}
def remove_file(_hash):
    os.remove(_hash + '.zip')
def download_sample(_hash):
    data = {
        'query': 'get_file',
        'sha256_hash': _hash,
    }
    max_retries = 1

    def make_request():
        try:
            resp = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=(5, 30), headers=headers,
                                 allow_redirects=True)
            resp.raise_for_status()  # Check for HTTP errors
            return resp
        except requests.exceptions.ReadTimeout as e:
            print(f"Read timeout: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def perform_request_with_retry():
        for attempt in range(max_retries):
            response = make_request()
            if response is not None:
                return response
            else:
                time.sleep(5)
        print(f"Maximum retries reached. Unable to complete the request.")
        return None

    response = perform_request_with_retry()
    if response is not None:
        if 'file_not_found' in response.text:
            print("404 error for " + _hash)
            return
        else:
            with open(_hash + '.zip', 'wb') as file:
                file.write(response.content)

            file_path = _hash + ".zip"
            try:
                with pyzipper.AESZipFile(file_path) as zf:
                    zf.pwd = PASSWORD
                    zf.extractall("D:/MalwareBazaarDownload/")
                    print(f"Sample `{_hash}` downloaded and unzipped")
            except pyzipper.zipfile.BadZipFile:
                print(f"Error: {file_path} is not a valid ZIP file. Continuing with the rest of the program.")

            remove_file(_hash)
    else:
        print("Request failed even after retries.")


def split_file(filename, num_parts):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Calculate the size of each part
    part_size = len(lines) // num_parts
    parts = [lines[i:i + part_size] for i in range(0, len(lines), part_size)]

    # Ensure the last part has the remaining lines (in case of uneven division)
    if len(parts) > num_parts:
        parts[-2].extend(parts[-1])  # Add remaining lines to the second last part
        parts = parts[:-1]

    return parts


def download_in_parallel(hashes):
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(download_sample, hashes)


def main():
    parts = split_file('result.txt', 8)

    # Download each part in parallel
    for part in parts:
        download_in_parallel([hash.strip() for hash in part])

    print("Download complete.")


if __name__ == "__main__":
    main()
