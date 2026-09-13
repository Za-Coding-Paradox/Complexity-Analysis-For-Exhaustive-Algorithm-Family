import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent.parent
DATA_PATH = BASE / 'dataset' / '2018.csv'
OUTPUT_PATH = BASE / 'dataset' / 'filtered' / 'dataset.csv'

columns_to_keep = [
    'FL_DATE',
    'OP_CARRIER',
    'ORIGIN',
    'DEST',
    'DEP_DELAY',
    'ARR_DELAY',
    'TAXI_IN',
    'TAXI_OUT',
    'AIR_TIME',
    'DISTANCE',
]


def filter_dataset():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH, usecols=columns_to_keep)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Rows:    {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    print(f"Saved to {OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    filter_dataset()