import arithmetic
import random


def rand():
    return arithmetic.Residue(random.randint(0, arithmetic.Q - 1))
