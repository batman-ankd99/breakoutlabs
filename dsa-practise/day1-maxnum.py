Day 1 (06-07-2026) — Problem: Find the Largest Number in a List
Statement:
Write a Python function that takes a list of integers and returns the largest number in it — without using Python's built-in max() function.

def max_num(num_list):
    if len(num_list) > 0:
        max_number = num_list[0]
    else:
        print("list is empty")
        return None
    for element in num_list:
        if element > max_number:
            max_number = element

    return max_number


a = []
n = int(input("enter length of list"))
for i in range(n):
  a.append(int(input("enter numbers in a list")))

max_num(a)
