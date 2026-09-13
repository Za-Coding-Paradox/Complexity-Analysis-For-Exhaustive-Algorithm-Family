def insertion_sort(arr):
    """
    Insertion Sort
    Best:    O(n)   already sorted, inner loop never executes
    Average: O(n²)
    Worst:   O(n²)  reverse sorted
    Stable:  Yes
    """
    arr = list(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr