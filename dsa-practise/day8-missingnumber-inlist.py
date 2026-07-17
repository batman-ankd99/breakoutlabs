Day 8 (12-07-2026) — Problem: Find the Missing Number

You're given a list containing n distinct integers taken from the range 0 to n (inclusive) — so the list has n elements but the range has n+1 possible values, meaning exactly one number is missing. Write a function that finds it.

Example:

Input: [3, 0, 1]
Output: 2
(Here n = 3, so the full range is 0..3. The list has 3 elements, and 2 is the one missing.)

Another example:

Input: [0, 1]
Output: 2
A few things to think about before you code:

Can you do this without sorting the list first?
There's an approach using sum of a range — what's the formula for the sum of 0 to n, and how would comparing it to the actual sum help?
Can you also think of a second approach (e.g. using XOR) as a mental exercise, even if you only implement one?
Give it a shot tomorrow and share your attempt first, as usual.

def missing_num(list_num):
    n = len(list_num) + 1
    sum_actual = 0
    sum_withmiss = 0
    for i in range(n):
        sum_actual += i
    for elem in list_num:
        sum_withmiss +=elem
    missing_elem = sum_actual - sum_withmiss
    return missing_elem

list1 = []
n = int(input("enter length of list"))
for i in range(n):
  elem = int(input("enter numbers in a list : "))
  list1.append(elem)

result = missing_num(list1)
print(result)
