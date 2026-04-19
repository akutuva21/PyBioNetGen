import timeit

def side_string_old(patterns):
    side_str = ""
    for ipat, pat in enumerate(patterns):
        if ipat > 0:
            side_str += " + "
        side_str += str(pat)
    return side_str

def side_string_new(patterns):
    return " + ".join(str(pat) for pat in patterns)

patterns = ["pat{}".format(i) for i in range(100)]

old_time = timeit.timeit(lambda: side_string_old(patterns), number=10000)
new_time = timeit.timeit(lambda: side_string_new(patterns), number=10000)

print(f"Old time: {old_time:.5f} s")
print(f"New time: {new_time:.5f} s")
