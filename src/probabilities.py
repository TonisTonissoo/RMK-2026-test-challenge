from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "ts093_traffic_accidents.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_events.csv"


ALL_ACCIDENTS = "Liiklusõnnetused"
FATAL_ACCIDENTS = "Hukkunuga liiklusõnnetused"
DRUNK_ACCIDENTS = "Liiklusõnnetused joobes mootorsõidukijuhi osalusel"
FATAL_DRUNK_ACCIDENTS = (
    "Hukkunuga liiklusõnnetused joobes mootorsõidukijuhi osalusel"
)


def load_data() -> pd.DataFrame:
    return pd.read_csv(INPUT_PATH)


def get_period_metrics(
    wide: pd.DataFrame,
    start_year: int,
    end_year: int,
) -> dict[str, float]:
    period = wide.loc[start_year:end_year]

    accidents = period[ALL_ACCIDENTS].sum()
    fatal = period[FATAL_ACCIDENTS].sum()
    drunk = period[DRUNK_ACCIDENTS].sum()
    fatal_drunk = period[FATAL_DRUNK_ACCIDENTS].sum()

    return {
        "p_drunk": drunk / accidents,
        "p_fatal": fatal / accidents,
        "p_fatal_given_drunk": fatal_drunk / drunk,
        "p_fatal_drunk": fatal_drunk / accidents,
    }


def calculate_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.pivot_table(
        index="Aasta",
        columns="Näitaja",
        values="value",
        aggfunc="sum",
    )

    early_period = get_period_metrics(wide, 2000, 2004)
    recent_period = get_period_metrics(wide, 2020, 2024)

    events = [
        {
            "event": "Drunk-driver accident share",
            "period": "2000–2004",
            "probability": early_period["p_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "drunk-driver accidents / all accidents",
        },
        {
            "event": "Drunk-driver accident share",
            "period": "2020–2024",
            "probability": recent_period["p_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "drunk-driver accidents / all accidents",
        },
        {
            "event": "Fatal accident risk",
            "period": "2000–2004",
            "probability": early_period["p_fatal"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal accidents / all accidents",
        },
        {
            "event": "Fatal accident risk",
            "period": "2020–2024",
            "probability": recent_period["p_fatal"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal accidents / all accidents",
        },
        {
            "event": "Fatality risk in drunk-driver accidents",
            "period": "2000–2004",
            "probability": early_period["p_fatal_given_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal drunk-driver accidents / drunk-driver accidents",
        },
        {
            "event": "Fatality risk in drunk-driver accidents",
            "period": "2020–2024",
            "probability": recent_period["p_fatal_given_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal drunk-driver accidents / drunk-driver accidents",
        },
        {
            "event": "Fatal drunk-driver accident share",
            "period": "2000–2004",
            "probability": early_period["p_fatal_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal drunk-driver accidents / all accidents",
        },
        {
            "event": "Fatal drunk-driver accident share",
            "period": "2020–2024",
            "probability": recent_period["p_fatal_drunk"],
            "source": "Statistics Estonia TS093",
            "calculation": "fatal drunk-driver accidents / all accidents",
        },
    ]

    return pd.DataFrame(events)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_data()
    probabilities = calculate_probabilities(df)

    print(probabilities)

    probabilities.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()