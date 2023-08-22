from FROST import *

VK = Company(2, 5)
print(check_Schnoor_signature(*VK.sign_stage("OK", [VK.users[0], VK.users[1], VK.users[2]])))