from pathlib import Path
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_events.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "probability_scale.png"


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    order = [
        "Drunk-driver accident share",
        "Fatal accident risk",
        "Fatality risk in drunk-driver accidents",
        "Fatal drunk-driver accident share",
    ]

    df["event"] = pd.Categorical(df["event"], categories=order, ordered=True)
    df = df.sort_values(["event", "period"]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    y_positions = []
    y_labels = []

    period_colors = {
        "2000–2004": "gray",
        "2020–2024": "navy",
    }

    for group_index, event_name in enumerate(order):
        group = df[df["event"] == event_name]
        base_y = group_index * 4

        for offset, (_, row) in enumerate(group.iterrows()):
            y = base_y + offset
            y_positions.append(y)

            one_in_n = round(1 / row["probability"])
            y_labels.append(
                f"{event_name}\n{row['period']} · about 1 in {one_in_n}"
            )

            color = period_colors.get(row["period"], "black")

            ax.hlines(
                y=y,
                xmin=0,
                xmax=row["probability"],
                linewidth=2,
                alpha=0.35,
                color=color,
            )

            ax.scatter(
                row["probability"],
                y,
                s=90,
                zorder=3,
                color=color,
            )

    ax.set_xlim(0, 0.25)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels)

    ax.set_xlabel("Probability (%)")
    ax.set_title("How Traffic Accident Risks Changed in Estonia", pad=16)

    ax.grid(axis="x", alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markerfacecolor="gray",
            color="gray",
            label="2000–2004",
            markersize=8,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markerfacecolor="navy",
            color="navy",
            label="2020–2024",
            markersize=8,
        ),
    ]

    ax.legend(handles=legend_elements, loc="upper right", frameon=False)

    plt.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()