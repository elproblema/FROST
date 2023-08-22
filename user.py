from arithmetic import *
from package import *


class User:

    def __init__(self, id):
        self.id = id
        self.d = None
        self.e = None  # d_self.id and e_self.id
        self.poly = None  # f_self.id(x)
        self.secret = Residue(0)  # equals to |s_self.id| in original article
        self.secret_packages = []  # There stored all securely sent packages to user with |self.id| id number

    @staticmethod
    def send_private_package(package, user):
        user.secret_packages.append(package)

    @staticmethod
    def send_public_package(package):
        match package.name:
            case "POLY":
                PublicPackage.keygen_packages.append(package)
            case "POK":
                PublicPackage.keygen_packages.append(package)
            case "ERN":
                PublicPackage.sign_packages.append(package)
            case "SIGN":
                PublicPackage.sign_packages.append(package)

    def collect_package(self, name, *args):
        match name:
            case "POLY":
                self.poly = Polynom(*args)
                package = POLYpackage(self.id)
                package.collect(self.poly)
                return package
            case "POK":
                package = POKpackage(self.id)
                package.collect(self.poly)
                return package
            case "PS":
                package = PSpackage(self.id)
                package.collect(*args, self.poly)
                return package
            case "ERN":
                package = ERNpackage(self.id)
                self.d = rand()
                self.e = rand()
                package.collect(self.d, self.e)
                return package
            case "SIGN":
                package = SIGNpackage(self.id)
                package.collect(self.d, self.e, self.secret, *args)
                return package

    def handle_private_packages(self):
        for package in self.secret_packages:
            if package.name == "PS":
                package.check(self.id)
                self.secret += package.value
