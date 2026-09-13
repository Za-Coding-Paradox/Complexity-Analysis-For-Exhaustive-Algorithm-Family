import pandas as pd
import numpy as np


# Part B - sample sizes
SAMPLE_SIZES = [100, 500, 1_000, 2_500, 5_000, 7_500, 10_000]


def draw_sample(df: pd.DataFrame, n: int, column: str) -> list:
    """
    Draws a random sample of n rows from df for the given column.
    Returns a list of values.
    """
    sample = df[column].dropna().sample(n=n, random_state=42).tolist()
    return sample


def get_orderings(sample: list) -> dict:
    """
    Generates three orderings from a sample:
      - random:   as drawn (average case)
      - sorted:   ascending (best case)
      - reversed: descending (worst case)
    """
    return {
        'random':   sample,
        'sorted':   sorted(sample),
        'reversed': sorted(sample, reverse=True),
    }


def generate_all_samples(df: pd.DataFrame, column: str) -> dict:
    """
    For every sample size, generate all 3 orderings.
    Returns a nested dict: {n: {ordering: [values]}}
    """
    all_samples = {}
    for n in SAMPLE_SIZES:
        sample = draw_sample(df, n, column)
        all_samples[n] = get_orderings(sample)
        print(f"Generated samples for n={n:,}")
    return all_samples


if __name__ == "__main__":
    from loader import load_dataset
    df = load_dataset()
    samples = generate_all_samples(df, 'ARR_DELAY')
    print(samples[100]['random'][:5])