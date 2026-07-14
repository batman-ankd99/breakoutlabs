Day 7 (11-07-2026) — Problem: Rotate a List by K Positions
Write a Python function that takes a list of integers and an integer k, and returns the list rotated to the right by k positions — without using slicing.
Example:
Input: list = [1, 2, 3, 4, 5], k = 2
Output: [4, 5, 1, 2, 3]

def rotate_list(list_num, k):
    rotated_list = []
    n = len(list_num)
    for i in range(n-k,n):
        rotated_list.append(list_num[i])
    print("original list ", list_num)
    for i in range(k+1):
        rotated_list.append(list_num[i])
    return rotated_list

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = int(input("enter numbers in a list : "))
  list1.append(elem)

result = rotate_list(list1, 2)
print(result)
