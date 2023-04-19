"""
Monte Carlo simulation for a famous lost boarding ticket problem
O(n**2) n - number of seats for one iteration
"""
import numpy as np


def simulate():
    n_seats = 100
    seats = [_ for _ in range(1, n_seats+1)]
    seats_set = set(seats)
    grandma_seat = np.random.choice(seats)
    seats_set.remove(grandma_seat)
    for i in range(2, n_seats):
        if i in seats_set:
            seats_set.remove(i)
        else:
            temp_seat = np.random.choice(list(seats_set))
            seats_set.remove(temp_seat)
    return 1 if n_seats in seats_set else 0




n_sims = 100000
result_sims = [-1 for _ in range(n_sims)]
for i in range(n_sims):
    result_sims[i] = simulate()

print(sum(result_sims)/n_sims)