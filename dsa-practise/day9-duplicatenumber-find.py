Day 9 (13-07-2026)— Problem: Find the Duplicate Number
Statement:
You're given a list of n+1 integers where every number is in the range 1 to n (inclusive). Exactly one number is repeated — it could appear two or more times, everything else appears exactly once. Write a function that finds the duplicate — without using a set() or sorting the list.
Example:
Input: [1, 3, 4, 2, 2]
Output: 2

def duplicate_num(num_list):
    number_dict = {}
    for elem in num_list:
        if elem in number_dict:
            number_dict[elem] += 1
            found_dup = elem
            break
        else:
            number_dict[elem] = 1
    return found_dup

result = duplicate_num([3,5,6,8,5])
print(result)
