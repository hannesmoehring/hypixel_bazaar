import json
import time
from datetime import datetime as dt

import requests

API_URL = "https://api.hypixel.net/v2/skyblock/bazaar"
DATA_DIR = "data"


def fetch_data_from_api(api):
    response = requests.get(api)
    return response


def save_data_to_json(data):
    time = dt.now().strftime("%d-%m_%H-%M")
    with open(f"{DATA_DIR}/data_{time}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def routine():
    print("Fetching data from API...")
    data = fetch_data_from_api(API_URL)
    if data.status_code == 200:
        print("Data fetched successfully.")
        data = data.json()
        save_data_to_json(data)
        print("Data saved to JSON file.")
    else:
        print("Failed to fetch data.")
        print(f"Error: {data.status_code}")

    print("\n-----------------------------------------------------------------------\n")


if __name__ == "__main__":
    while True:
        routine()
        time.sleep(600)
