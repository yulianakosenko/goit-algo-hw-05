def binary_search_upper_bound(arr, x):
    left, right = 0, len(arr) - 1
    iterations = 0
    result = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] == x:
            result = arr[mid]
            right = mid - 1  # шукаємо найменший індекс для "верхньої межі"
        elif arr[mid] < x:
            left = mid + 1
        else:
            result = arr[mid]
            right = mid - 1

    # Якщо result None, значить всі елементи < x, верхньої межі немає
    if result is None:
        # Верхня межа — найменший елемент більший за x, якщо він є
        if left < len(arr):
            result = arr[left]
        else:
            result = None  # немає верхньої межі

    return (iterations, result)

#Приклад:
arr = [1.1, 2.5, 3.3, 4.4, 5.5]
print(binary_search_upper_bound(arr, 3.0))
