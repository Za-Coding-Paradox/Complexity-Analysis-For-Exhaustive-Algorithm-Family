import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

# Part B - sample sizes
SAMPLE_SIZES = [100, 500, 1_000, 2_500, 5_000, 7_500, 10_000]


def draw_sample(df: pd.DataFrame, n: int, column: str) -> list:
    """
    Draws a random sample of n rows from df for the given column.
    Returns a list of values.
    """
    log.info(f"Drawing sample of n={n:,} from column '{column}'")
    sample = df[column].dropna().sample(n=n, random_state=42).tolist()
    log.info(f"Sample drawn successfully | n={n:,}")
    return sample


def get_orderings(sample: list) -> dict:
    """
    Generates three orderings from a sample:
      - random:   as drawn (average case)
      - sorted:   ascending (best case)
      - reversed: descending (worst case)
    """
    log.info("Generating 3 orderings: random, sorted, reversed")
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
    log.info(f"Generating samples for column '{column}' across sizes: {SAMPLE_SIZES}")
    all_samples = {}
    for n in SAMPLE_SIZES:
        sample = draw_sample(df, n, column)
        all_samples[n] = get_orderings(sample)
        log.info(f"Ready: n={n:,} with all 3 orderings")
    log.info("All samples generated")
    return all_samples


if __name__ == "__main__":
    from loader import load_dataset
    df = load_dataset()
    samples = generate_all_samples(df, 'ARR_DELAY')
    print(samples[100]['random'][:5])