from bionetgen.modelapi.structs import Action

a = Action('generate_network', {'max_stoich': 'not a dict'})
print(a.args)
