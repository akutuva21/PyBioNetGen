import timeit
setup = 'rule = [["0"], ["1"]]'
test_list = 'tmp1 = rule[0] if rule[0] not in ["0", ["0"]] else []'
test_tuple = 'tmp1 = rule[0] if rule[0] not in ("0", ["0"]) else []'
print("List:", timeit.timeit(test_list, setup=setup, number=10000000))
print("Tuple:", timeit.timeit(test_tuple, setup=setup, number=10000000))
