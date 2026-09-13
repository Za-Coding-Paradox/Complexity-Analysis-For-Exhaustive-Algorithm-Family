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
FILTERED_PATH = BASE / 'dataset' / 'filtered' / 'dataset.csv'


def load_dataset() -> pd.DataFrame:
    """
    Part A - Loads the filtered dataset from disk using chunked reading.
    Reports row count, columns, and memory footprint of one chunk.
    """
    chunk_size = 100_000
    chunks = []
    total_rows = 0
    first_chunk = True

    log.info(f"Loading dataset from {FILTERED_PATH}")
    log.info(f"Chunk size: {chunk_size:,} rows")

    for chunk in pd.read_csv(FILTERED_PATH, chunksize=chunk_size):
        if first_chunk:
            mem = chunk.memory_usage(deep=True).sum() / 1e6
            log.info(f"Columns: {list(chunk.columns)}")
            log.info(f"First chunk memory footprint: {mem:.2f} MB")
            first_chunk = False
        chunks.append(chunk)
        total_rows += len(chunk)
        log.info(f"Loaded {total_rows:,} rows so far...")

    df = pd.concat(chunks, ignore_index=True)

    missing_pct = df['ARR_DELAY'].isnull().mean() * 100
    log.info(f"Total rows loaded:      {total_rows:,}")
    log.info(f"ARR_DELAY min:          {df['ARR_DELAY'].min()}")
    log.info(f"ARR_DELAY max:          {df['ARR_DELAY'].max()}")
    log.info(f"ARR_DELAY mean:         {df['ARR_DELAY'].mean():.2f}")
    log.info(f"ARR_DELAY missing:      {missing_pct:.2f}%")

    return df


if __name__ == "__main__":
    df = load_dataset()
    print(df.head())