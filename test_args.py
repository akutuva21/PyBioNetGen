from bionetgen.modelapi.structs import Action

try:
    a = Action('generate_network', {'max_stoich': 'not a dict'})
except Exception as e:
    print(e)
