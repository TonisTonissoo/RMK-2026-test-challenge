from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_events.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "probability_scale.png"


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    df = df.sort_values("probability", ascending=True).reset_index(drop=True)

    df["one_in_n"] = (1 / df["probability"]).round().astype(int)
    df["label"] = df.apply(
        lambda row: f"{row['event']}  ·  about 1 in {row['one_in_n']}",
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(11, 5))

    y_positions = range(len(df))

    ax.hlines(
        y=y_positions,
        xmin=df["probability"].min() / 1.5,
        xmax=df["probability"],
        linewidth=2,
        alpha=0.5,
    )

    ax.scatter(df["probability"], y_positions, s=90, zorder=3)

    ax.set_xscale("log")
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["label"])

    ax.set_xlabel("Probability, logarithmic scale")
    ax.set_title("Probability Scale of Traffic Accident Risks", pad=16)

    ax.grid(axis="x", which="both", alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()