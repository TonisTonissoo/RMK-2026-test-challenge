from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_events.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "probability_scale.png"

KEY_EVENT = "Fatality risk in drunk-driver accidents"


def one_in_n(probability: float) -> str:
    return f"1 in {round(1 / probability)}"


def format_change(change: float) -> str:
    if abs(change) < 0.10:
        return "≈ unchanged"
    if change < 0:
        return f"↓ {abs(change):.0%}"
    return f"↑ {change:.0%}"


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    order = (
        df.groupby("event")["probability"]
        .mean()
        .sort_values(ascending=True)
        .index
    )

    wide = df.pivot(
        index="event",
        columns="period",
        values="probability",
    ).loc[order]

    changes = (wide["2020–2024"] - wide["2000–2004"]) / wide["2000–2004"]

    fig, ax = plt.subplots(figsize=(12, 7))
    x_max = wide.max().max()

    y_positions = range(len(order))

    for y, event in zip(y_positions, order):
        old = wide.loc[event, "2000–2004"]
        new = wide.loc[event, "2020–2024"]
        change = changes.loc[event]

        is_key_event = event == KEY_EVENT
        line_color = "darkred" if is_key_event else "lightgray"
        new_color = "darkred" if is_key_event else "navy"

        ax.plot(
            [old, new],
            [y, y],
            color=line_color,
            linewidth=3.5 if is_key_event else 3,
            alpha=0.45 if is_key_event else 1,
            zorder=1,
        )

        ax.scatter(
            old,
            y,
            s=125 if is_key_event else 110,
            color="gray",
            label="2000–2004" if y == 0 else "",
            zorder=3,
        )

        ax.scatter(
            new,
            y,
            s=150 if is_key_event else 110,
            color=new_color,
            label="2020–2024" if y == 0 else "",
            zorder=4,
        )

        ax.text(
            max(old, new) + (x_max * 0.03),
            y,
            format_change(change),
            va="center",
            fontsize=11,
            fontweight="bold",
            color="darkred" if is_key_event else "black",
        )

        ax.text(
            old,
            y + 0.18,
            one_in_n(old),
            ha="center",
            va="bottom",
            fontsize=9,
            color="gray",
        )

        if y == 0:
            new_y_offset = -0.10
        else:
            new_y_offset = -0.18

        ax.text(
            new,
            y + new_y_offset,
            one_in_n(new),
            ha="center",
            va="top",
            fontsize=9,
            color=new_color,
        )

    pretty_labels = [
        label.replace("accident share", "share").replace(
            "Fatality risk in drunk-driver accidents",
            "Fatality risk (drunk-driving)",
        )
        for label in order
    ]

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(pretty_labels)

    ax.set_xlim(0, x_max * 1.35)
    ax.set_ylim(-0.35, len(order) - 0.65)

    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax.set_xlabel("Probability of event")
    ax.set_title(
        "Safer Roads — But Drunk-Driving Still Deadly",
        pad=18,
        fontsize=16,
    )

    ax.text(
        0,
        -0.72,
        "Most traffic risks fell by roughly 60%, but drunk-driver accidents remained almost as likely to be fatal.",
        fontsize=10,
        color="dimgray",
        transform=ax.transAxes,
    )

    ax.grid(axis="x", alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.legend(loc="upper right", frameon=False)

    plt.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=220, bbox_inches="tight")
    plt.close()

    print(f"Saved plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()