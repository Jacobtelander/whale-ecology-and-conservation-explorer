import requests
import pandas as pd


def fetch_whale_data():
    url = "https://api.obis.org/v3/occurrence"

    params = {
        "scientificname": "Megaptera novaeangliae",
        "size": 300
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["results"]

    df = pd.DataFrame(data)

    df = df[
        [
            "scientificName",
            "decimalLatitude",
            "decimalLongitude",
            "eventDate"
        ]
    ]

    df = df.dropna()

    df = df.rename(
        columns={
            "scientificName": "species",
            "decimalLatitude": "latitude",
            "decimalLongitude": "longitude",
            "eventDate": "date"
        }
    )

    df.to_csv("data/whales.csv", index=False)

    print("Saved whale data to data/whales.csv")
    print(df.head())


fetch_whale_data()