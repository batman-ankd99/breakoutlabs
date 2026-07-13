Day 6 (10-07-2026) — Problem: Find All Pairs That Sum to a Target
Statement:
Write a Python function that takes a list of integers and a target sum, and returns all unique pairs of numbers from the list that add up to the target — without using nested loops (no for i inside for j).
Example:
pythonInput: list = [2, 7, 4, 1, 5, 3], target = 6
Output: [(2, 4), (1, 5)]


def target_sum(list_num, target):
    pairs = []
    for i in range(len(list_num)-1):
        if list_num[i] + list_num[i+1] == 10:
            pairs.append((i,j))

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = int(input("enter numbers in a list : "))
  list1.append(elem)

target_sum(list1, 10)
