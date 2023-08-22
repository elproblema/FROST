from arithmetic import *
import math
from hash_functions import *

# Package is class that represents
# interaction between users during protocol FROST

# Fields of the class are the only information that need to be sent

# Method check is used to check correctness (according to original article) of the package

# Method collect is used to conveniently create correct package

class Package:
    def abort(self):
        print(f"Package from user #{self.id} with name {self.name} is incorrect! Log: {self.log}")
        exit(1)

    def check(self, *args):
        pass

    def collect(self, *args):
        pass


class PublicPackage(Package):
    keygen_packages = []  # this would be storage for all packages
    # that was sent publicly in our model during KeyGen stage
    sign_packages = []  # this would be storage for all packages
    # that was sent publicly in our model during Preprocess and Sign stages


class PrivatePackage(Package):
    pass


def search(id=None, name=None, stage="KG"):  # function that searches package with certain name and user-id
    return next(filter(lambda pack: ((pack.id == id)
                                or (id is None))
                               and ((pack.name == name)
                                or (name is None)),
                       PublicPackage.keygen_packages if stage == "KG" else
                       PublicPackage.sign_packages))


class POLYpackage(PublicPackage):
    def __init__(self, id):
        self.poly = None
        self.name = "POLY"
        self.log = ""
        self.id = id

    def collect(self, poly: Polynom):  # "poly" must be Polynom instance with coefficients from Z_Q
        self.poly = poly.secure()

    def check(self):
        pass


class POKpackage(PublicPackage):  # POK - proof of knowledge
    def __init__(self, id):
        self.R = None
        self.u = None  # greek "mu" in original article
        self.id = id
        self.log = ""
        self.name = "POK"

    def collect(self, poly: Polynom):  # "poly" must be Polynom instance with coefficients from Z_Q
        k = rand()
        self.R = Order(k)
        c = hash(self.id, "there you should use context string", Order(poly.A[0]), self.R)
        self.u = k + poly.A[0] * c

    def check(self):
        poly_package = search(self.id, "POLY")
        c = hash(self.id, "there you should use context string", poly_package.poly.A[0], self.R)
        if Order(self.u) != poly_package.poly.A[0] * c + self.R:
            self.abort()


class PSpackage(PrivatePackage):  # PS - Private shares
    def __init__(self, id):
        self.id = id
        self.name = "PS"
        self.value = None
        self.point = None
        self.log = ""

    def collect(self, point: Residue, poly: Polynom):
        self.point = point
        self.value = poly.evaluate(point)

    def check(self, id):  # here "id" argument stands for receiver user-id that will be checking this package
        poly_package = search(self.id, "POLY")
        if Order(self.value) != poly_package.poly.evaluate(id):
            self.log = str(id)
            self.abort()


def calculate_public_key():  # calculates Y from the original article
    return sum((package.poly.A[0]
                if package.name == "POLY"
                else Order(0)
                for package in PublicPackage.keygen_packages), Order(0))


class ERNpackage(PublicPackage):  # ERN - Encrypted random nonces
    def __init__(self, id):
        self.D = None
        self.E = None
        self.log = ""
        self.id = id
        self.name = "ERN"

    def collect(self, d, e):
        self.D = Order(d)
        self.E = Order(e)

    def check(self, *args):
        pass

    def __str__(self):
        return str(self.D) + str(self.E)


def calculate_lagrange_coefficient(pi, S):
    res = Residue(1)
    for pj in S:
        res *= (Residue(pj.id) / (Residue(pj.id) - Residue(pi.id))
         if pj.id != pi.id
         else Residue(1))
    return res


def ro_calculate(id, m, B):
    ro = hash1(id, m, *B)
    return ro


def calculate_R(m, B, S):
    return sum((pack.D + pack.E * ro_calculate(user.id, m, B) for (user, pack) in zip(S, B)), Order(0))


class SIGNpackage(PublicPackage):
    def __init__(self, id):
        self.id = id
        self.name = "SIGN"
        self.log = ""
        self.z = None

    def collect(self, d, e, s, m, B, S):
        ro = ro_calculate(self.id, m, B)
        c = hash2(calculate_R(m, B, S), calculate_public_key(), m)
        self.z = d + e * ro + (s * calculate_lagrange_coefficient(self, S)) * c

    def check(self, *args):
        pass
