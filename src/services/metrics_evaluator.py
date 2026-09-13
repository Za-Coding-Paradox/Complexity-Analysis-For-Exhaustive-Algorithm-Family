import time
import math
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.selection_sort import selection_sort
from services.loader import load_dataset
from services.chunker import generate_all_samples, SAMPLE_SIZES

RESULTS_PATH = Path(__file__).parent.parent / 'results' / 'metrics.csv'
GRAPHS_PATH  = Path(__file__).parent.parent / 'results'

ALGORITHMS = {
    'bubble_sort':    bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
}


def benchmark(samples: dict) -> list:
    """
    Part D: Times every algorithm on every sample size and ordering.
    Returns a list of result rows.
    """
    results = []
    total = len(SAMPLE_SIZES) * 3 * 3
    done = 0

    for n, orderings in samples.items():
        for ordering, data in orderings.items():
            for algo_name, algo_fn in ALGORITHMS.items():
                start = time.perf_counter()
                algo_fn(data)
                elapsed = time.perf_counter() - start

                results.append({
                    'size':        n,
                    'ordering':    ordering,
                    'algorithm':   algo_name,
                    'time_seconds': round(elapsed, 6),
                })
                done += 1
                print(f"[{done}/{total}] {algo_name} | n={n:,} | {ordering} → {elapsed:.4f}s")

    return results


def benchmark_text(df: pd.DataFrame, n: int) -> list:
    """
    Part D: Repeat one sample size on the text column (OP_CARRIER).
    """
    from services.chunker import draw_sample, get_orderings
    sample = draw_sample(df, n, 'OP_CARRIER')
    orderings = get_orderings(sample)
    results = []

    for ordering, data in orderings.items():
        for algo_name, algo_fn in ALGORITHMS.items():
            start = time.perf_counter()
            algo_fn(data)
            elapsed = time.perf_counter() - start

            results.append({
                'size':        n,
                'ordering':    ordering,
                'algorithm':   algo_name,
                'column':      'OP_CARRIER (text)',
                'time_seconds': round(elapsed, 6),
            })
            print(f"[TEXT] {algo_name} | n={n:,} | {ordering} → {elapsed:.4f}s")

    return results


def save_results(results: list):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv(RESULTS_PATH, index=False)
    print(f"\nSaved results to {RESULTS_PATH}")
    return df


def plot_results(df: pd.DataFrame):
    GRAPHS_PATH.mkdir(parents=True, exist_ok=True)

    # Chart 1: runtime vs n for each algorithm on random ordering
    fig, ax = plt.subplots(figsize=(10, 6))
    random_df = df[df['ordering'] == 'random']
    for algo in ALGORITHMS:
        subset = random_df[random_df['algorithm'] == algo]
        ax.plot(subset['size'], subset['time_seconds'], marker='o', label=algo)
    ax.set_title('Runtime vs Sample Size (Random Ordering)')
    ax.set_xlabel('Sample Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(GRAPHS_PATH / 'chart1_runtime_vs_n.png')
    print("Saved chart1_runtime_vs_n.png")

    # Chart 2: insertion sort across all 3 orderings
    fig, ax = plt.subplots(figsize=(10, 6))
    insertion_df = df[df['algorithm'] == 'insertion_sort']
    for ordering in ['random', 'sorted', 'reversed']:
        subset = insertion_df[insertion_df['ordering'] == ordering]
        ax.plot(subset['size'], subset['time_seconds'], marker='o', label=ordering)
    ax.set_title('Insertion Sort: Runtime by Ordering')
    ax.set_xlabel('Sample Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(GRAPHS_PATH / 'chart2_insertion_sort_orderings.png')
    print("Saved chart2_insertion_sort_orderings.png")


def format_time(seconds: float) -> str:
    """Converts seconds into the most readable unit."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 86400 * 365:
        return f"{seconds / 86400:.2f} days"
    else:
        return f"{seconds / (86400 * 365):.2f} years"


def extrapolate(df: pd.DataFrame, full_n: int):
    """
    Part E: Extrapolates runtime to full dataset scale.

    - Fits time = c * n^2 for each algorithm using the largest sample
    - Estimates full dataset sort time
    - Compares to Timsort O(n log n)
    """
    print("\n" + "=" * 60)
    print("Part E: Extrapolation to Full Scale")
    print(f"Full dataset size: {full_n:,} rows")
    print("=" * 60)

    largest_n = SAMPLE_SIZES[-1]
    random_df = df[(df['ordering'] == 'random') & (df['size'] == largest_n)]

    timsort_results = {}

    for algo in ALGORITHMS:
        row = random_df[random_df['algorithm'] == algo]
        if row.empty:
            print(f"\n  {algo}: no data found for n={largest_n:,}")
            continue

        t_measured = row['time_seconds'].values[0]

        # Fit c from: t = c * n^2  =>  c = t / n^2
        c = t_measured / (largest_n ** 2)

        # Extrapolate to full dataset
        t_full = c * (full_n ** 2)

        print(f"\n  {algo}")
        print(f"    Measured at n={largest_n:,}:   {t_measured:.6f}s")
        print(f"    Constant c = t / n^2:       {c:.2e}")
        print(f"    Estimated full sort time:   {format_time(t_full)}")

        timsort_results[algo] = t_full

    # Timsort estimate: use bubble_sort's c as baseline clock speed reference
    # Timsort: t = c_machine * n * log2(n)
    # Estimate c_machine from bubble_sort measurement
    baseline_row = random_df[random_df['algorithm'] == 'bubble_sort']
    if not baseline_row.empty:
        t_measured = baseline_row['time_seconds'].values[0]
        # operations per second from bubble sort
        ops_per_sec = (largest_n ** 2) / t_measured
        timsort_ops = full_n * math.log2(full_n)
        t_timsort = timsort_ops / ops_per_sec

        print(f"\n  timsort (estimated)")
        print(f"    Estimated full sort time:   {format_time(t_timsort)}")

        print("\n  Speedup factors over Timsort:")
        for algo, t_full in timsort_results.items():
            speedup = t_full / t_timsort
            print(f"    {algo}: {speedup:,.0f}x slower than Timsort")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    df_raw = load_dataset()

    # Numeric benchmarks
    samples = generate_all_samples(df_raw, 'ARR_DELAY')
    results = benchmark(samples)

    # Text benchmark on n=1000
    text_results = benchmark_text(df_raw, 1_000)
    results.extend(text_results)

    results_df = save_results(results)
    plot_results(results_df)

    # Part E: full dataset row count from loader
    full_n = len(df_raw)
    extrapolate(results_df, full_n)