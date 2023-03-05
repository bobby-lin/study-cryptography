"""
Exercise: https://cryptohack.org/courses/elliptic/ecc1/
Equation: Y^2 = X^3 + 497X + 1768, p: 9739

Zero point is not on the curve and has no corresponding x and y values.
In programs, we represent it as (0, 0) but it should be thought as infinity.

From: An Introduction to Mathematical Cryptography", Jeffrey Hoffstein, Jill Pipher, Joseph H. Silverman
(a) If P = O, then P + Q = Q.
(b) Otherwise, if Q = O, then P + Q = P.
(c) Otherwise, write P = (x1, y1) and Q = (x2, y2).
(d) If x1 = x2 and y1 = −y2, then P + Q = O.
(e) Otherwise:
  (e1) if P ≠ Q: λ = (y2 - y1) / (x2 - x1)
  (e2) if P = Q: λ = (3x1^2 + a) / 2y1
(f) x3 = λ2 − x1 − x2,     y3 = λ(x1 −x3) − y1
(g) P + Q = (x3, y3)
"""
import math


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def print(self):
        print(f"({self.x}, {self.y})")


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def get_lhs(self, y):
        return int(math.pow(y, 2) % self.p)

    def get_rhs(self, x):
        return int((math.pow(x, 3) + self.a * x + self.b) % self.p)

    def extended_gcd(self, a, b):
        """
        Calculates the extended Euclidean algorithm for finding the greatest common divisor (gcd) of a and b,
        as well as the coefficients x and y such that ax + by = gcd(a, b).
        Returns a tuple (gcd, x, y).
        """
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def multiplicative_inverse(self, a):
        """
        Calculates the multiplicative inverse of a modulo m using the extended Euclidean algorithm.
        Returns the inverse of a modulo m, or None if a and m are not coprime.
        """
        # Calculate gcd(a, m) and check if they are coprime
        gcd, x, y = self.extended_gcd(a, self.p)
        if gcd != 1:
            return None  # a and m are not coprime, so there is no inverse

        # Calculate the inverse using the extended Euclidean algorithm
        inverse = x % self.p
        return inverse

    def calculate_m(self, p, q):
        prime = self.p
        a = self.a

        if p.x != q.x and p.y != q.y:
            if q.x - p.x < 0:
                return int(((p.y - q.y) * self.multiplicative_inverse(p.x - q.x)) % prime)
            else:
                return int(((q.y - p.y) * self.multiplicative_inverse(q.x - p.x)) % prime)
        else:
            return int(((3 * math.pow(p.x, 2) + a) * self.multiplicative_inverse(2 * p.y)) % prime)

    def add(self, p, q):
        prime = self.p
        a = self.a

        if p.x == 0 and p.y == 0:
            return q
        if q.x == 0 and q.y == 0:
            return p
        if p.x == q.x and p.y == (-1 * q.y):
            return Point(0, 0)

        m = self.calculate_m(p, q)
        result_x = (math.pow(m, 2) - p.x - q.x) % prime
        result_y = (m * (p.x - result_x) - p.y) % prime

        return Point(result_x, result_y)


curve = EllipticCurve(497, 1768, 9739)

x = Point(5274, 2841)
y = Point(8669, 740)

ans = curve.add(x, y)
ans.print()

P = Point(493, 5564)
Q = Point(1539, 4742)
R = Point(4403, 5202)

point_1 = curve.add(P, P)
point_2 = curve.add(point_1, Q)
point_3 = curve.add(point_2, R)
point_3.print()

print("====Check answer====")
print(f"{curve.get_lhs(point_3.y)} = {curve.get_rhs(point_3.x)}")