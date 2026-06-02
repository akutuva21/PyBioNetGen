import sys

with open("bionetgen/atomizer/sbml2bngl.py", "r") as f:
    content = f.read()

content = content.replace("""                        # TODO: if for whatever reason a rate rule
                        # was defined as a parameter that is not 0
                        # remove it. This might not be exact behavior
                        if re.search(r"^{0}\s".format(rawArule[0]), element):
                            logMess(
                                "WARNING:SIM106",
                                "Parameter {0} corresponds both as a non zero parameter \\
                            and a rate rule, verify behavior".format(
                                    element
                                ),
                            )
                            removeParameters.append(element)""", """                        # Note: if for whatever reason a rate rule
                        # was defined as a parameter that is not 0
                        # remove it. This might not be exact behavior
                        if re.search(r"^{0}\s".format(rawArule[0]), element):
                            logMess(
                                "WARNING:SIM106",
                                "Parameter {0} corresponds both as a non zero parameter \\
                            and a rate rule, removing parameter".format(
                                    element
                                ),
                            )
                            removeParameters.append(element)""")

with open("bionetgen/atomizer/sbml2bngl.py", "w") as f:
    f.write(content)
