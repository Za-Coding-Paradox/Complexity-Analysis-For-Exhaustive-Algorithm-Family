def bubble_sort(arr):
    """
    Bubble Sort
    Best:    O(n)  already sorted, early exit triggers
    Average: O(n²)
    Worst:   O(n²) reverse sorted
    Stable:  Yes
    """
    arr = list(arr)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr