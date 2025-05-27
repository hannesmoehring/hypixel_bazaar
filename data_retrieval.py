import json
import time
from datetime import datetime as dt

import requests

API_URL_MAYOR = "https://api.hypixel.net/v2/resources/skyblock/election"
API_URL_BAZAAR = "https://api.hypixel.net/v2/skyblock/bazaar"
DATA_DIR_BAZAAR = "data/bz"
DATA_DIR_MAYOR = "data/mayor"


def fetch_data_bazaar(api, time):
    data = requests.get(api)
    if data.status_code == 200:
        print("Data fetched successfully for BAZAAR.")
        data = data.json()
        save_data_to_json(data, DATA_DIR_BAZAAR, time)
        print("Data saved to JSON file.")
    else:
        print("Failed to fetch data for BAZAAR.")
        print(f"Error: {data.status_code}")


def fetch_data_mayor(api, time):
    data = requests.get(api)

    if data.status_code == 200:
        print("Data fetched successfully for MAYOR.")
        data = data.json()
        save_data_to_json(data, DATA_DIR_MAYOR, time)
        print("Data saved to JSON file.")
    else:
        print(data)
        print("Failed to fetch data for MAYOR.")
        print(f"Error: {data.status_code}")



def save_data_to_json(data, dir, time:str):
    with open(f"{dir}/data_{time}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def routine():
    time = dt.now().strftime("%d-%m_%H-%M")
 
    print(f"Fetching data from API at {time}...")
    fetch_data_bazaar(API_URL_BAZAAR, time)
    fetch_data_mayor(API_URL_MAYOR, time)
    print("\n-----------------------------------------------------------------------\n")


if __name__ == "__main__":
    while True:
        try:
            routine()
            time.sleep(300)
        except Exception as e:
            print(e)
