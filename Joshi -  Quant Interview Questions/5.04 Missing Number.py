"""
Find missing number in first N numbers given some N-1 numbers
"""

N = 5
nums = [1, 2, 3, 5]

nums_sum = 0
for i in range(N-1):
    nums_sum += nums[i]

art_sum = (1+N) * N / 2

print(nums_sum - art_sum)
