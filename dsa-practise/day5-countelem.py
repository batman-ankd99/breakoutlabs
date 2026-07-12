Day 5 (09-07-2026) — Problem: Count Occurrences of Each Element
Statement:
Write a Python function that takes a list of integers and returns a dictionary showing how many times each element appears — without using collections.Counter.
Example:
pythonInput: [4, 2, 4, 5, 2, 4, 7, 1]
Output: {4: 3, 2: 2, 5: 1, 7: 1, 1: 1}

def count_elem(list_num):
    dict_elem = {}
    for elem in list_num:
        if elem in dict_elem:
            dict_elem[elem] += 1
        else:
            dict_elem[elem] = 1
    return dict_elem

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = int(input("enter numbers in a list : "))
  list1.append(elem)


result = count_elem(list1)
print(result)
