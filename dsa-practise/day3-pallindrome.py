Day 3 (07-07-2026) — Problem: Check if a List is a Palindrome
Statement:
Write a Python function that takes a list (of integers) and returns True if it reads the same forwards and backwards, and False otherwise — without using slicing (list[::-1]) or the built-in reversed().

def pallin_2(list_num):
    rev_num = []
    for i in range(len(list_num)-1,-1,-1):
      rev_num.append(list_num[i])

    if list_num == rev_num:
      print("list is pallindrome")
    else:
      print("it is not")



def pallin_1(list_num):
    is_pallin = True
    for i in range(len(list_num)//2):
      if list_num[i] != list_num[len(list_num)-1-i]:
        is_pallin = False
        break
    if is_pallin:
      print("List of numbers is pallindrome")
    else:
      print("List is not a pallindrome")

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = input("enter numbers in a list : ")
  list_num.append(elem)

pallin_1(list1)
pallin_2(list1)
