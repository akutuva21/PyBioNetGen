from bionetgen.modelapi.structs import Action

a = Action('generate_network', {'max_stoich': {'A': 5}})
print(a.args)
