from bionetgen.modelapi.structs import Action

a = Action('generate_network', {'max_stoich': [1,2,3]})
print(a.args)
