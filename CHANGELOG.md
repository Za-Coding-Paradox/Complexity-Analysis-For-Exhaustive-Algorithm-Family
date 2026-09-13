# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-09-13

### Added
- Bubble sort, selection sort, and insertion sort implementations
- Chunked dataset loading with memory reporting (Part A)
- Random sample generation with 3 orderings: random, sorted, reversed (Part B)
- Full benchmarking pipeline with `time.perf_counter()` (Part D)
- CSV export of all timing results as `sort_benchmark_results.csv`
- Chart 1: runtime vs sample size (random ordering)
- Chart 2: insertion sort runtime by ordering (best/average/worst case)
- Chart 3: numeric vs text column runtime comparison
- Part E extrapolation: fits `time = c * n²`, estimates full dataset sort time
- Timsort comparison and speedup factor calculation
- Logging across all modules
- Interactive CLI menu with dataset loaded flag and screen clearing
- Dataset filtering to relevant columns
- Column properties inspector