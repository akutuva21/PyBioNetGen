parameters = ["k1 10.0", "k2 0.0"]
removeParameters = []
rawArule = ["k1"]

import re

for element in parameters:
    if re.search(r"^{0}\s".format(rawArule[0]), element):
        removeParameters.append(element)

param = [x for x in parameters if x not in removeParameters]
print(param)
