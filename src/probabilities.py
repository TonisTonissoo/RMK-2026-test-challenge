from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "ts093_traffic_accidents.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_events.csv"


def load_traffic_data() -> pd.DataFrame:
    return pd.read_csv(INPUT_PATH)


def calculate_2024_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    latest_year = 2024

    year_data = df[df["Aasta"] == latest_year]

    wide = year_data.pivot_table(
        index="Aasta",
        columns="Näitaja",
        values="value",
        aggfunc="sum",
    ).reset_index()

    all_accidents = wide.loc[0, "Liiklusõnnetused"]
    fatal_accidents = wide.loc[0, "Hukkunuga liiklusõnnetused"]
    drunk_accidents = wide.loc[
        0, "Liiklusõnnetused joobes mootorsõidukijuhi osalusel"
    ]
    fatal_drunk_accidents = wide.loc[
        0, "Hukkunuga liiklusõnnetused joobes mootorsõidukijuhi osalusel"
    ]

    events = [
        {
            "event": "A traffic accident involves a drunk driver",
            "probability": drunk_accidents / all_accidents,
            "source": "Statistics Estonia TS093, 2024",
            "calculation": f"{drunk_accidents} / {all_accidents}",
        },
        {
            "event": "A traffic accident is fatal",
            "probability": fatal_accidents / all_accidents,
            "source": "Statistics Estonia TS093, 2024",
            "calculation": f"{fatal_accidents} / {all_accidents}",
        },
        {
            "event": "A traffic accident is fatal and involves a drunk driver",
            "probability": fatal_drunk_accidents / all_accidents,
            "source": "Statistics Estonia TS093, 2024",
            "calculation": f"{fatal_drunk_accidents} / {all_accidents}",
        },
    ]

    return pd.DataFrame(events)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_traffic_data()
    probabilities = calculate_2024_probabilities(df)
    probabilities.to_csv(OUTPUT_PATH, index=False)

    print(probabilities)
    print(f"Saved probability events to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()