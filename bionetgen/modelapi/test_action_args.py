from bionetgen.modelapi.structs import Action

try:
    a = Action('generate_network', {'max_stoich': 'not a dict'})
    print("Failed: Should have raised an error!")
except Exception as e:
    print(f"Success! Raised: {e}")
