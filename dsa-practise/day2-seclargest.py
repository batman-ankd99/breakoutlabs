Day 2 (07-07-2026) — Problem: Find the Second Largest Number in a List
Statement:
Write a Python function that takes a list of integers and returns the second largest number in it — without using Python's built-in max() or sorted()/sort().

a = []
n = int(input("enter length of list"))
for i in range(n):
  a.append(int(input("enter numbers in a list")))

def second_largest(list1):
    if len(list1) < 2:
        print("list dont have 2 elements")
        return None

    max_num = list1[0]
    second_num = list1[0]

    for element in list1:
        if element > max_num:
            second_num = max_num
            max_num = element
        elif element < max_num and element >= second_num:
            second_num = element
    return second_num
