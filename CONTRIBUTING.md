# Contributing

## Getting Started

1. Fork the repository
2. Clone your fork
3. Set up the environment:

```bash
uv python pin 3.12
uv add pandas matplotlib kaggle
```

## Project Structure

- `src/algorithms/` — sorting implementations, one file per algorithm
- `src/services/` — core pipeline: loading, sampling, benchmarking
- `src/operations/` — data preparation utilities
- `src/results/` — generated outputs, not committed to version control

## Guidelines

**Algorithms**
- No use of built-in `sort()` or `sorted()` inside algorithm files
- Every algorithm must work on both numeric and string data
- Every algorithm must have a docstring with best, average, worst case complexity and stability

**Code Style**
- Use `logging` for all status output, not bare `print()` except for final reports
- Use `pathlib.Path` for all file paths
- Use `time.perf_counter()` for all timing measurements

**Adding a New Algorithm**
1. Create a new file in `src/algorithms/`
2. Implement the function with a full docstring
3. Import and add it to the `ALGORITHMS` dict in `metrics_evaluator.py`
4. The benchmarking pipeline will pick it up automatically

## Running the Project

```bash
uv run python src/menu.py
```

## Pull Requests

- Keep pull requests focused on one change
- Update `CHANGELOG.md` with what you changed
- Make sure the full pipeline runs without errors before submitting