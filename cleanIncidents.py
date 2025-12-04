from pathlib import Path
import pandas as pd

INCIDENTS_DIR = Path("/Users/johnnybae/Documents/Academia/Chaminade/DS495 - Research/Incidents")

# final column names
FINAL_COLS = [
    "ID", "Vic-Killed", "Vic-Injured",
    "Sus-Killed", "Sus-Injured", "Sus-Unharmed", "Sus-Arrested",
    "Characteristics",
]

# map source to final names
RENAME_MAP = {
    "Incident ID": "ID",
    "# Victims Killed": "Vic-Killed",
    "# Victims Injured": "Vic-Injured",
    "# Suspect Killed": "Sus-Killed",
    "# Suspects Injured": "Sus-Injured",
    "# Suspects Unharmed": "Sus-Unharmed",
    "# Suspects Arrested": "Sus-Arrested",
    "Incident Characteristics": "Characteristics",
}

def clean_one(csv_path: Path) -> Path:
    out_path = csv_path.with_name(f"{csv_path.stem}_clean.csv")
    try:
        df = pd.read_csv(csv_path, low_memory=False)
        # keep only columns we know how to rename
        df = df[[c for c in RENAME_MAP if c in df.columns]].rename(columns=RENAME_MAP)
        # ensure all final cols exist in order, fill blanks with "N/A"
        df = df.reindex(columns=FINAL_COLS).fillna("N/A")
        df.to_csv(out_path, index=False)
        print(f"[OK] {csv_path.name} → {out_path.name}  rows={len(df)}")
    except Exception as e:
        print(f"[SKIP] {csv_path.name}: {e}")
    return out_path

def main():
    csvs = sorted(INCIDENTS_DIR.glob("*.csv"))
    if not csvs:
        print(f"No CSV files found in {INCIDENTS_DIR}")
        return
    print(f"Found {len(csvs)} incident CSVs in {INCIDENTS_DIR}")
    for csv in csvs:
        # skip already-cleaned files
        if csv.name.endswith("_clean.csv"):
            continue
        clean_one(csv)

if __name__ == "__main__":
    main()