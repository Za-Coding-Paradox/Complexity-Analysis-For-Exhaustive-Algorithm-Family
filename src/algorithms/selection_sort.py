def selection_sort(arr):
    """
    Selection Sort
    Best:    O(n²) no early exit, always scans full remaining list
    Average: O(n²)
    Worst:   O(n²)
    Stable:  No
    """
    arr = list(arr)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr