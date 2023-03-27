"""
Write an algorithm derived from uniform distribution to retrieve RV from weighted discrete distribution
O(n) - complexity for 1 retrieval, n - number of states of RV
"""
import numpy as np

# set of states with probabilities
states = [(123, 0.3), (93, 0.4), (13, 0.2), (-20, 0.1)]

# simulate N times
N = 1000
total_sum = 0
for i in range(N):
    # take the uniform RV
    x = np.random.uniform(0, 1)
    sum_prob = 0
    asset = None

    # check whether x is in between the probabilities
    for state in states:
        sum_prob += state[1]
        if x < sum_prob:
            asset = state[0]
            break
    total_sum += asset

# compute expectation
print(total_sum/N)

'''
If N is very big we can find cumulative sum first and use rounding of X uniform RV with appropriate precision
It is based on https://en.wikipedia.org/wiki/Inverse_transform_sampling
'''