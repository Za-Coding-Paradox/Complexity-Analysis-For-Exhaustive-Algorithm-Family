import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from operations.filter_dataset import filter_dataset
from operations.list_columns import list_columns

_loaded_df = None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("\n" + "=" * 50)
    print("   Data Complexity Analysis")
    print("=" * 50)


def print_menu():
    status = "loaded" if _loaded_df is not None else "not loaded"
    print(f"\n  Dataset status: [{status}]")
    print("\n  OPERATIONS")
    print("  1. List dataset columns & properties")
    print("  2. Filter dataset")
    print("\n  ANALYSIS")
    print("  3. Load filtered dataset")
    print("  4. Run benchmarks (all algorithms)")
    print("  5. View results & graphs")
    print("\n  0. Exit")
    print("-" * 50)


def handle_choice(choice: str):
    global _loaded_df

    if choice == "1":
        clear()
        print("\n-> Listing columns...\n")
        list_columns()

    elif choice == "2":
        clear()
        print("\n-> Filtering dataset...\n")
        filter_dataset()

    elif choice == "3":
        clear()
        if _loaded_df is not None:
            print("\n  Dataset already loaded. Skipping.")
        else:
            from services.loader import load_dataset
            print("\n-> Loading filtered dataset...\n")
            _loaded_df = load_dataset()

    elif choice == "4":
        clear()
        from services.chunker import generate_all_samples
        from services.metrics_evaluator import benchmark, benchmark_text, save_results, plot_results, extrapolate

        if _loaded_df is None:
            from services.loader import load_dataset
            print("\n-> Dataset not loaded. Loading now...\n")
            _loaded_df = load_dataset()

        print("\n-> Running benchmarks...\n")
        samples = generate_all_samples(_loaded_df, 'ARR_DELAY')
        results = benchmark(samples)
        text_results = benchmark_text(_loaded_df, 1_000)
        results.extend(text_results)
        results_df = save_results(results)
        plot_results(results_df)
        extrapolate(results_df, len(_loaded_df))

    elif choice == "5":
        clear()
        import pandas as pd
        results_path = Path(__file__).parent / 'results' / 'metrics.csv'
        if not results_path.exists():
            print("\n  No results found. Run benchmarks first (option 4).")
        else:
            df = pd.read_csv(results_path)
            print("\n-> Results summary:\n")
            print(df.to_string(index=False))

    elif choice == "0":
        clear()
        print("\nExiting. Goodbye!\n")
        sys.exit(0)

    else:
        print("\n  Invalid option. Try again.")


def main():
    while True:
        clear()
        print_header()
        print_menu()
        choice = input("Enter option: ").strip()
        handle_choice(choice)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()