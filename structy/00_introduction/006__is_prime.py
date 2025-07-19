import math


def is_prime(n):
    if n == 1:
        return False
    elif n < 4:
        return True
    elif n % 2 == 0:
        return False
    elif n < 9:
        return True
    elif n % 3 == 0:
        return False
    else:
        r = math.floor(math.sqrt(n))
        f = 5
        for f in range(5, r + 1, 6):
            if n % f == 0:
                return False
            if n % (f + 2) == 0:
                return False
        return True
