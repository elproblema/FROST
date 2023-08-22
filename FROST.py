from user import *
from hash_functions import *

class Company:  # This class plays SA-role in sign stage

    def __init__(self, t, n):  # this is keygen stage
        self.users = [User(id + 1) for id in range(n)]
        for user in self.users:
            User.send_public_package(user.collect_package("POLY", t))
            User.send_public_package(user.collect_package("POK"))
        for package in PublicPackage.keygen_packages:
            package.check()
        for user_from in self.users:
            for user_to in self.users:
                User.send_private_package(user_from.collect_package("PS", user_to.id), user_to)
        for user in self.users:
            user.handle_private_packages()

    def sign_stage(self, m, S):  # S - set of members that wants to sign, m - message that needed to be signed
        PublicPackage.sign_packages.clear()
        for user in S:
            User.send_public_package(user.collect_package("ERN"))
        B = [search(user.id, "ERN", stage="SIGN") for user in S]
        for user in S:
            User.send_public_package(user.collect_package("SIGN", m, B, S))
        z = sum((search(user.id, "SIGN", "SIGN").z for user in S), Residue(0))
        return z, calculate_R(m, B, S), calculate_public_key(), m


def check_Schnoor_signature(z, R, Y, m):
    c = hash2(R, Y, m)
    return Order(z) == R + Y * c
