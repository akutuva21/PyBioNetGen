import time as time_mod
import numpy as np
import os

def _write_bng_dat_original(path, time, data_2d, col_names):
    headers = ["time"] + list(col_names)
    with open(path, "w") as f:
        f.write("# " + "  ".join(f"{h:>18s}" for h in headers) + "\n")
        for i in range(len(time)):
            vals = [time[i]] + [data_2d[i, j] for j in range(data_2d.shape[1])]
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

def _write_bng_dat_new(path, time, data_2d, col_names):
    headers = ["time"] + list(col_names)
    with open(path, "w") as f:
        f.write("# " + "  ".join(f"{h:>18s}" for h in headers) + "\n")
        for i, t in enumerate(time):
            vals = [t] + [data_2d[i, j] for j in range(data_2d.shape[1])]
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

def _write_bng_dat_new2(path, time, data_2d, col_names):
    headers = ["time"] + list(col_names)
    with open(path, "w") as f:
        f.write("# " + "  ".join(f"{h:>18s}" for h in headers) + "\n")
        for i, t in enumerate(time):
            vals = [t] + data_2d[i].tolist()
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

def _append_bng_dat_rows_original(path, time, data_2d, skip_first=True):
    start = 1 if (skip_first and len(time) > 0) else 0
    with open(path, "a") as f:
        for i in range(start, len(time)):
            vals = [time[i]] + [data_2d[i, j] for j in range(data_2d.shape[1])]
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

def _append_bng_dat_rows_new(path, time, data_2d, skip_first=True):
    start = 1 if (skip_first and len(time) > 0) else 0
    with open(path, "a") as f:
        for i, t in enumerate(time[start:], start=start):
            vals = [t] + [data_2d[i, j] for j in range(data_2d.shape[1])]
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

def _append_bng_dat_rows_new2(path, time, data_2d, skip_first=True):
    start = 1 if (skip_first and len(time) > 0) else 0
    with open(path, "a") as f:
        for i, t in enumerate(time[start:], start=start):
            vals = [t] + data_2d[i].tolist()
            f.write("  ".join(f"{v:22.12e}" for v in vals) + "\n")

time = np.linspace(0, 100, 10000)
data_2d = np.random.rand(10000, 50)
col_names = [f"S{i}" for i in range(50)]

print("Testing _write_bng_dat:")
t0 = time_mod.time()
_write_bng_dat_original("test_orig.dat", time, data_2d, col_names)
t1 = time_mod.time()
print(f"Original: {t1 - t0:.4f} seconds")

t0 = time_mod.time()
_write_bng_dat_new("test_new.dat", time, data_2d, col_names)
t1 = time_mod.time()
print(f"New (enumerate): {t1 - t0:.4f} seconds")

t0 = time_mod.time()
_write_bng_dat_new2("test_new2.dat", time, data_2d, col_names)
t1 = time_mod.time()
print(f"New2 (enumerate + tolist): {t1 - t0:.4f} seconds")

print("\nTesting _append_bng_dat_rows:")
t0 = time_mod.time()
_append_bng_dat_rows_original("test_orig.dat", time, data_2d)
t1 = time_mod.time()
print(f"Original: {t1 - t0:.4f} seconds")

t0 = time_mod.time()
_append_bng_dat_rows_new("test_new.dat", time, data_2d)
t1 = time_mod.time()
print(f"New (enumerate): {t1 - t0:.4f} seconds")

t0 = time_mod.time()
_append_bng_dat_rows_new2("test_new2.dat", time, data_2d)
t1 = time_mod.time()
print(f"New2 (enumerate + tolist): {t1 - t0:.4f} seconds")

os.remove("test_orig.dat")
os.remove("test_new.dat")
os.remove("test_new2.dat")
