"""
Write an algorithms which caries numerical integration:
Use the concept of Riemann sums
"""

class Riemann:

    def __init__(self):
        self.par_a = 1
        self.par_b = 0
        self.par_c = 0
    def parabola(self, x):
        """Sample quadratic function"""
        return self.par_a*x**2 + self.par_b*x + self.par_c

    def set_parabola(self, a, b, c):
        self.par_a = a
        self.par_b = b
        self.par_c = c

    def integrate(self, func, lower_bound, upper_bound, n=1000):
        """Use left Riemann sums"""
        increment = (upper_bound-lower_bound)/n
        increments = [lower_bound + _ * increment for _ in range(n)]
        left_sum = 0
        for inc in increments:  # could use np.arange(a, b, (b-a)/n)
            left_sum += func(inc)
        left_sum *= increment  # normalize the sum
        return left_sum


R = Riemann()
a, b, c = 1, 2, 3
R.set_parabola(a, b, c)

lower_bound = 3
upper_bound = 5
print(R.integrate(R.parabola, lower_bound, upper_bound))




