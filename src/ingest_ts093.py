from pathlib import Path

import pandas as pd
import requests
from pyjstat import pyjstat


API_URL = "https://andmed.stat.ee/api/v1/et/stat/TS093"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "ts093_traffic_accidents.csv"


def fetch_ts093() -> pd.DataFrame:
    query = {
        "query": [
            {
                "code": "Näitaja",
                "selection": {
                    "filter": "item",
                    "values": ["1", "2", "3", "4"],
                },
            },
            {
                "code": "Kuu",
                "selection": {
                    "filter": "item",
                    "values": ["00"],
                },
            },
        ],
        "response": {"format": "json-stat2"},
    }

    response = requests.post(API_URL, json=query, timeout=30)
    response.raise_for_status()

    dataset = pyjstat.Dataset.read(response.text)
    return dataset.write("dataframe")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = fetch_ts093()
    print(df.head())
    print(df.columns)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()