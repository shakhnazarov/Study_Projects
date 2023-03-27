import math
"""
Fib numbers numerating from 0
"""
# Naive algorithm
def fib(n):
    if n in {0, 1}:
        return 1
    else:
        return fib(n-1) + fib(n-2)


N = 80

# Memory efficient algorithm
fib_seq = [1, 1, 2]
for i in range(3, N+1):
    fib_seq[0], fib_seq[1] = fib_seq[1], fib_seq[2]
    fib_seq[2] = fib_seq[1] + fib_seq[0]


# O(1) using closed-form and rounding  (or O(logN) given multiplication), incorrect results for high N
golden = (1+math.sqrt(5))/2
golden_n = pow(golden, N+1)
print("Binet rounding", round(golden_n / math.sqrt(5)))

# O(1) without rounding
golden = (1+math.sqrt(5))/2
conjugate = (1-math.sqrt(5))/2
golden_n = pow(golden, N+1)
conjugate_n = pow(conjugate, N+1)
print("Binet", round((golden_n - conjugate_n)/math.sqrt(5)))

# DP
print("DP", fib_seq[min(N, 2)])
# print(fib(N))