import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent.parent
FILTERED_PATH = BASE / 'dataset' / 'filtered' / 'dataset.csv'


def load_dataset() -> pd.DataFrame:
    """
    Part A - Loads the filtered dataset from disk.
    Reports row count, columns, and memory footprint of one chunk.
    """
    chunk_size = 100_000
    chunks = []
    total_rows = 0
    first_chunk = True

    for chunk in pd.read_csv(FILTERED_PATH, chunksize=chunk_size):
        if first_chunk:
            print(f"Columns:          {list(chunk.columns)}")
            print(f"Chunk memory:     {chunk.memory_usage(deep=True).sum() / 1e6:.2f} MB")
            first_chunk = False
        chunks.append(chunk)
        total_rows += len(chunk)

    df = pd.concat(chunks, ignore_index=True)

    print(f"Total rows:       {total_rows:,}")
    print(f"Missing ARR_DELAY: {df['ARR_DELAY'].isnull().mean() * 100:.2f}%")
    print(f"ARR_DELAY min:    {df['ARR_DELAY'].min()}")
    print(f"ARR_DELAY max:    {df['ARR_DELAY'].max()}")
    print(f"ARR_DELAY mean:   {df['ARR_DELAY'].mean():.2f}")

    return df


if __name__ == "__main__":
    df = load_dataset()
    print(df.head())