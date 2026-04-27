# Probability Scale of Traffic Accident Risks in Estonia

Test challenge submission for the RMK Data Team Internship 2026.

## Overview

This project explores how to build intuition about probability by placing real-world events on a shared logarithmic probability scale.

Using open data from Statistics Estonia, I estimate probabilities for several traffic accident related events and compare them with simple baseline reference events.

The goal is not only to calculate probabilities, but to make them interpretable.

---

## Events Included

Current probability scale includes:

| Event | Approximate Probability | Intuition |
|------|--------------------------|-----------|
| Coin flip | 0.50 | 1 in 2 |
| Traffic accident involves a drunk driver | 0.063 | 1 in 16 |
| Traffic accident is fatal | 0.033 | 1 in 30 |
| A 1-in-100 reference event | 0.010 | 1 in 100 |
| Traffic accident is fatal and involves a drunk driver | 0.005 | 1 in 191 |

---

## Data Source

Primary data source:

Statistics Estonia API  
Table TS093 — Inimkannatanutega liiklusõnnetused teedel (kuud)

API endpoint:

https://andmed.stat.ee/api/v1/et/stat/TS093

Indicators used:

- Traffic accidents
- Fatal traffic accidents
- Traffic accidents involving a drunk driver
- Fatal traffic accidents involving a drunk driver

Data extracted programmatically using Python and the Statistics Estonia API.

---

## Method

Probabilities were calculated from 2024 event counts using simple frequency ratios.

Example:

Probability that a traffic accident is fatal:

P(fatal | accident) = fatal accidents / all accidents

64 / 1914 ≈ 0.033

Probability that a traffic accident involves a drunk driver:

121 / 1914 ≈ 0.063

Events are visualized on a logarithmic probability scale.

---

## Repository Structure

```text
data/
├── raw/
│   └── ts093_traffic_accidents.csv
│
└── processed/
    └── probability_events.csv

src/
├── ingest_ts093.py
├── probabilities.py
└── plot.py

outputs/
└── probability_scale.png
```

---

## Run Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

Fetch source data:

```bash
python src/ingest_ts093.py
```

Calculate probabilities:

```bash
python src/probabilities.py
```

Generate visualization:

```bash
python src/plot.py
```

---

## Example Output

Generated probability scale:

`outputs/probability_scale.png`

---

## Assumptions and Limitations

- Probabilities are estimated from aggregated event frequencies.
- 2024 is used as a first approximation and may contain yearly variation.
- Some baseline reference events (coin flip, 1-in-100 event) are included only to improve interpretability.
- This is a probability intuition exercise, not a formal risk model.

Future improvement:
- Use multi-year averages instead of a single year.
- Add additional Estonian public datasets for broader comparisons.
- Explore Bayesian or conditional probability extensions.

---

## Why This Approach

This solution prioritizes:

- programmatic reproducibility  
- transparent assumptions  
- interpretable visualization  
- simple but extensible code

The emphasis is on statistical intuition rather than complexity.

---

## License

MIT