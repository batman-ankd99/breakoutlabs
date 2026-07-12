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


list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = input("enter numbers in a list : ")
  list1.append(elem)
