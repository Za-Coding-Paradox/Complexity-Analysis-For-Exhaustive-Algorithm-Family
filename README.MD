# Complexity-Analysis-For-Exhaustive-Algorithm-Family

Empirical analysis of Bubble Sort, Selection Sort, and Insertion Sort
on the U.S. Airline Delay and Cancellation Dataset (2009–2018).

## Overview

This project benchmarks three O(n²) sorting algorithms against a real-world
dataset of ~7GB of flight records. It measures runtime across different sample
sizes and input orderings, extrapolates to full-scale performance, and compares
against Python's built-in Timsort.

## Dataset

U.S. Airline Delay and Cancellation Data, 2009–2018
Source: https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018

Download the dataset and place the CSV files under `dataset/`.

## Project Structure

```
src/
  algorithms/         # Sorting algorithm implementations
    bubble_sort.py
    selection_sort.py
    insertion_sort.py
  operations/         # Data preparation utilities
    filter_dataset.py
    list_columns.py
  services/           # Core pipeline
    loader.py         # Chunked dataset loading (Part A)
    chunker.py        # Sample generation (Part B)
    metrics_evaluator.py  # Benchmarking, charts, extrapolation (Parts D & E)
  results/            # Generated outputs
    sort_benchmark_results.csv
    chart1_runtime_vs_n.png
    chart2_insertion_sort_orderings.png
    chart3_numeric_vs_text.png
  menu.py             # Interactive CLI menu
dataset/
  filtered/           # Filtered dataset output
```

## Setup

```bash
uv init
uv python pin 3.12
uv add pandas matplotlib kaggle
```

## Usage

Run the interactive menu:

```bash
uv run python src/menu.py
```

Menu options:
```
1. List dataset columns & properties
2. Filter dataset
3. Load filtered dataset
4. Run benchmarks (all algorithms)
5. View results & graphs
```

Or run the full pipeline directly:

```bash
uv run python src/services/metrics_evaluator.py
```

## Columns Used

| Column      | Type    | Purpose              |
|-------------|---------|----------------------|
| ARR_DELAY   | numeric | Primary sort column  |
| OP_CARRIER  | text    | Text sort comparison |

## Sample Sizes

`100, 500, 1,000, 2,500, 5,000, 7,500, 10,000`

## Results

Outputs saved to `src/results/`:
- `sort_benchmark_results.csv` — all timing results
- `chart1_runtime_vs_n.png` — runtime vs sample size
- `chart2_insertion_sort_orderings.png` — insertion sort by ordering
- `chart3_numeric_vs_text.png` — numeric vs text comparison

## License

MIT