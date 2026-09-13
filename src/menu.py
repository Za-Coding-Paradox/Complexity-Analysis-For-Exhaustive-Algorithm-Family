import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from operations.filter_dataset import filter_dataset
from operations.list_columns import list_columns


def print_header():
    print("\n" + "=" * 50)
    print("   Data Complexity Analysis")
    print("=" * 50)


def print_menu():
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
    if choice == "1":
        print("\n-> Listing columns...\n")
        list_columns()

    elif choice == "2":
        print("\n-> Filtering dataset...\n")
        filter_dataset()

    elif choice == "3":
        from services.loader import load_dataset
        print("\n-> Loading filtered dataset...\n")
        load_dataset()

    elif choice == "4":
        from services.loader import load_dataset
        from services.chunker import generate_all_samples
        from services.metrics_evaluator import benchmark, benchmark_text, save_results, plot_results
        print("\n-> Running benchmarks...\n")
        df = load_dataset()
        samples = generate_all_samples(df, 'ARR_DELAY')
        results = benchmark(samples)
        text_results = benchmark_text(df, 1_000)
        results.extend(text_results)
        results_df = save_results(results)
        plot_results(results_df)

    elif choice == "5":
        import pandas as pd
        results_path = Path(__file__).parent / 'results' / 'metrics.csv'
        if not results_path.exists():
            print("\n  No results found. Run benchmarks first (option 4).")
        else:
            df = pd.read_csv(results_path)
            print("\n-> Results summary:\n")
            print(df.to_string(index=False))

    elif choice == "0":
        print("\nExiting. Goodbye!\n")
        sys.exit(0)

    else:
        print("\n  Invalid option. Try again.")


def main():
    while True:
        print_header()
        print_menu()
        choice = input("Enter option: ").strip()
        handle_choice(choice)


if __name__ == "__main__":
    main()