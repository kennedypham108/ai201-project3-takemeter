# Dataset Collection Instructions

## 1. Install the dependency

```bash
python3 -m pip install -r requirements.txt
```

## 2. Run the collector

```bash
python3 collect_reddit_data.py
```

The script searches public `r/nba` threads about LeBron James and creates:

```text
unlabeled_lebron_comments.csv
```

## 3. Label every row manually

Open the CSV in Google Sheets or Excel. For each row, enter exactly one label:

- `Evidence-Based Analysis`
- `Reasoned Opinion`
- `Hot Take or Reaction`

Use the `notes` column for difficult examples.

## 4. Save the final file

Rename the reviewed file:

```text
labeled_dataset.csv
```

The final CSV must contain at least 200 reviewed examples. Do not submit AI-generated or blank rows as collected Reddit data.
