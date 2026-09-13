import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

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
    log.info(f"Reading from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, usecols=columns_to_keep)
    log.info(f"Loaded {len(df):,} rows")
    log.info(f"Columns: {list(df.columns)}")
    df.to_csv(OUTPUT_PATH, index=False)
    log.info(f"Saved filtered dataset to {OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    filter_dataset()