from bionetgen.atomizer.writer.bnglWriter import bnglFunction
import time

rule = "lambda(a, b, a + b)"
# Baseline check for many iterations
start = time.time()
for _ in range(1000):
    bnglFunction(rule, "myFunc", [], [], {}, {})
end = time.time()
print("Time taken:", end - start)
