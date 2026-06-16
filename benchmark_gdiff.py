import timeit

setup_code = """
class DummyBNGGdiff:
    def _get_node_text(self, node):
        noded = node["data"]["y:ProxyAutoBoundsNode"]["y:Realizers"]
        for key in noded.keys():
            if "y:" in key:
                return noded[key]["y:NodeLabel"]["#text"]
        return None

class OptimizedBNGGdiff:
    def _get_node_text(self, node):
        noded = node["data"]["y:ProxyAutoBoundsNode"]["y:Realizers"]
        for key in noded:
            if "y:" in key:
                return noded[key]["y:NodeLabel"]["#text"]
        return None

node = {
    "data": {
        "y:ProxyAutoBoundsNode": {
            "y:Realizers": {
                "dummy1": "test",
                "dummy2": "test",
                "dummy3": "test",
                "dummy4": "test",
                "dummy5": "test",
                "y:GroupNode": {
                    "y:NodeLabel": {
                        "#text": "Success"
                    }
                }
            }
        }
    }
}
dummy = DummyBNGGdiff()
optimized = OptimizedBNGGdiff()
"""

test_dummy = "dummy._get_node_text(node)"
test_optimized = "optimized._get_node_text(node)"

num_runs = 1000000

dummy_time = timeit.timeit(test_dummy, setup=setup_code, number=num_runs)
optimized_time = timeit.timeit(test_optimized, setup=setup_code, number=num_runs)

print(f"Baseline time: {dummy_time:.4f} seconds")
print(f"Optimized time: {optimized_time:.4f} seconds")
print(f"Improvement: {(dummy_time - optimized_time) / dummy_time * 100:.2f}%")
