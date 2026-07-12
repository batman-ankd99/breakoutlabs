Day 4 (08-07-2026) — Problem: Remove Duplicates from a List
Statement:
Write a Python function that takes a list of integers and returns a new list with duplicates removed, preserving the original order of first occurrence — without using set().
Example:
pythonInput: [4, 2, 4, 5, 2, 7, 4, 1]
Output: [4, 2, 5, 7, 1]


def unique(list_num):
    unique_list = []
    for elem in list_num:
        if elem not in unique_list:
            unique_list.append(elem)
    return unique_list

def unique_faster(list1_num):
    unique_list = []
    seen = {}

    for elem in list1_num:
           if elem in seen:
               pass
           else:
               unique_list.append(elem)
               seen[elem] = "yes"

    return unique_list

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = int(input("enter numbers in a list : "))
  list1.append(elem)

result = unique_faster(list1)
print(result)
