from pathlib import Path
import pandas as pd

PARTICIPANTS_DIR = Path("/Users/johnnybae/Documents/Academia/Chaminade/DS495 - Research/Participants")

# final column names
FINAL_COLS = ["ID", "Date", "State", "City", "Gender", "Age Group"]

# map source → final names
RENAME_MAP = {
    "Incident ID": "ID",
    "Date": "Date",
    "State": "State",
    "City": "City",
    "Gender": "Gender",
    "Age Group": "Age Group",
}

def clean_one(csv_path: Path) -> Path:
    out_path = csv_path.with_name(f"{csv_path.stem}_clean.csv")
    try:
        df = pd.read_csv(csv_path, low_memory=False)
        # keep only columns we know how to rename
        df = df[[c for c in RENAME_MAP if c in df.columns]].rename(columns=RENAME_MAP)
        # ensure all final cols exist and in order, then fill blanks with "N/A"
        df = df.reindex(columns=FINAL_COLS).fillna("N/A")
        df.to_csv(out_path, index=False)
        print(f"[OK] {csv_path.name} → {out_path.name}  rows={len(df)}")
    except Exception as e:
        print(f"[SKIP] {csv_path.name}: {e}")
    return out_path

def main():
    csvs = sorted(PARTICIPANTS_DIR.glob("*.csv"))
    if not csvs:
        print(f"No CSV files found in {PARTICIPANTS_DIR}")
        return
    print(f"Found {len(csvs)} participants CSVs in {PARTICIPANTS_DIR}")
    for csv in csvs:
        # skip already-cleaned files
        if csv.name.endswith("_clean.csv"):
            continue
        clean_one(csv)

if __name__ == "__main__":
    main()
