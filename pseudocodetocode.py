def sortAndFindMedian(numbers):
    if not numbers:
        return "List is empty"
    # Step 1: Sort the numbers
    sorted_numbers = sortNumbers(numbers)
    n = len(sorted_numbers)

    # Step 2: Calculate and return the median
    if n % 2 == 0:
        return (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    return sorted_numbers[n // 2]

def sortNumbers(numbers):
    if len(numbers) <= 1:
        return numbers

    # Split the array into halves
    mid = len(numbers) // 2
    left = sortNumbers(numbers[:mid])
    right = sortNumbers(numbers[mid:])

    # Merge the sorted halves
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# Example usage
numbers1 = []  # Empty list
numbers2 = [9, 2, 6, 3]
print("Input: {}\n".format(numbers1))
print("Median: {}\n\n".format(sortAndFindMedian(numbers1)))

print("Input: {}\n".format(numbers2))
print("Median: {}\n\n".format(sortAndFindMedian(numbers2)))