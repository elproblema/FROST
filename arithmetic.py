Q = 89  # size of multiplicative group G (must be prime)
G_mod = 179 # field modulo G_mod generates multiplicative group with elements from Z_G_mod*


def extended_gcd(x, y):
    if y == 0:
        return 1, 0
    a, b = extended_gcd(y, x % y)
    k = x // y
    return b, a - b * k


class Residue:

    def __init__(self, r, mod=Q):
        if isinstance(r, Residue):
            self.r = r.r
            self.mod = r.mod
        elif isinstance(mod, Residue):
            self.r = r % mod.mod
            self.mod = mod.mod
        else:
            self.r = r % mod
            self.mod = mod

    def __add__(self, other):
        return Residue((self.r + other.r) % self.mod, self)

    def __sub__(self, other):
        return Residue((self.r - other.r) % self.mod, self)

    def __mul__(self, other):
        return Residue((self.r * other.r) % self.mod, self)

    def __neg__(self):
        return Residue(-self.r, self)

    def __pow__(self, power: int, modulo=None):
        bit = 0
        base = Residue(self)
        res = Residue(1, self)
        while 1 << bit <= power:
            if (1 << bit) & power:
                res *= base
            base *= base
            bit += 1
        return res

    def inverted(self):
        return Residue(extended_gcd(self.r, self.mod)[0] % self.mod, self)

    def __truediv__(self, other):
        return self * other.inverted()

    def __str__(self):
        return f"{self.r} mod {self.mod}"

    def __int__(self):
        return self.r

    def __eq__(self, other):
        return self.r == other.r

# arithmetics in class Order works unusual
# a + b = g^(x + y) where a = g^x and b = g^y
# -a = g^(-x) where a = g^x
# a * b = g^(x * b) where a = g^x


class Order:
    g = Residue(4, G_mod)  # generator of group G

    def __init__(self, x, is_order=False):  # Order(x) transforms x from Z_q to multiplicative group G (Order(x) = g^x)
        if isinstance(x, Order):
            self.ord = x.ord
        elif not is_order:
            self.ord = self.g ** int(x)
        else:
            self.ord = x

    def __neg__(self):
        return Order(self.ord.inverted(), is_order=True)

    def __add__(self, other):
        return Order(self.ord * other.ord, is_order=True)

    def __mul__(self, other: Residue):  # should be careful here, product is not commutative
        return Order(self.ord ** int(other), is_order=True)

    def __str__(self):
        return str(self.ord)

    def __int__(self):
        return int(self.ord)

    def __eq__(self, other):
        return self.ord == other.ord


from rand import *


# Polynom class works with Z_Q and multiplicative group with size of Q at the same time
# For class Residue Polynom works as usual polynomials
# For class Order it works like that
# We assume that f(x) = a_0 + a_1 * x + ... + a_t * x^t
# Polynomial.evaluate(x0) returns g^f(x0) if coefficients are g^a_0, g^a_1, ..., g^a_t

class Polynom:

    def __init__(self, A):
        if isinstance(A, int):
            self.A = [rand() for i in range(A)]
        else:
            self.A = A

    def evaluate(self, x):
        base = Residue(1)
        res = Order(0) if isinstance(self.A[0], Order) else Residue(0)
        for a_i in self.A:   # could be optimized for orders
            res += a_i * base
            base *= Residue(x)
        return res

    def secure(self): # returns Polynomial "transformed" to group G
        return Polynom([Order(a_i) for a_i in self.A])
