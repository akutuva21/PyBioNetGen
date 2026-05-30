import re


def replace():
    with open("bionetgen/atomizer/sbml2bngl.py", "r") as f:
        content = f.read()

    target = """                        self.arule_map[rawArule[0]] = name + "_ar"
                        self.only_assignment_dict[name] = name + "_ar"
                        if name in observablesDict:
                            observablesDict[name] = name + "_ar"
                        self.bngModel.add_arule(arule_obj)
                        continue"""

    replacement = """                        self.arule_map[rawArule[0]] = name + "_ar"
                        self.only_assignment_dict[name] = name + "_ar"
                        self.bngModel.add_arule(arule_obj)
                        continue"""

    if target in content:
        content = content.replace(target, replacement)
        with open("bionetgen/atomizer/sbml2bngl.py", "w") as f:
            f.write(content)
            print("Replaced redundant observable dict update.")
    else:
        print("Not found.")


replace()
