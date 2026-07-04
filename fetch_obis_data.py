import pandas as pd
import requests

SPECIES = {
    "Humpback Whale": "Megaptera novaeangliae",
    "Blue Whale": "Balaenoptera musculus",
    "Fin Whale": "Balaenoptera physalus",
    "Gray Whale": "Eschrichtius robustus",
    "Sperm Whale": "Physeter macrocephalus",
    "Minke Whale": "Balaenoptera acutorostrata",
}


def fetch_whale_data():

    all_data = []

    for common_name, scientific_name in SPECIES.items():

        print(f"Downloading {common_name}...")

        url = "https://api.obis.org/v3/occurrence"

        params = {
            "scientificname": scientific_name,
            "size": 1000,
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        results = response.json()["results"]

        if not results:
            continue

        df = pd.DataFrame(results)

        columns = [
            "scientificName",
            "decimalLatitude",
            "decimalLongitude",
            "eventDate",
        ]

        available = [c for c in columns if c in df.columns]

        df = df[available]

        df = df.rename(
            columns={
                "scientificName": "species",
                "decimalLatitude": "latitude",
                "decimalLongitude": "longitude",
                "eventDate": "date",
            }
        )

        df["common_name"] = common_name

        all_data.append(df)

    whales = pd.concat(all_data, ignore_index=True)

    whales = whales.dropna()

    whales.to_csv("data/whales.csv", index=False)

    print()
    print(f"Saved {len(whales):,} observations.")
    print()
    print(whales["common_name"].value_counts())


if __name__ == "__main__":
    fetch_whale_data()