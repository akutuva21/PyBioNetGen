import os

# Find VERSION file
vpath = os.path.dirname(os.path.abspath(__file__))
vpath = os.path.split(vpath)[0]
vpath = os.path.join(*[vpath, "assets", "VERSION"])
with open(vpath, "r") as f:
    v = f.read()
vtuple = [0, 0, 0, 0, 0]
for iv, ver in enumerate(v.split()):
    try:
        vtuple[iv] = int(ver)
    except:
        vtuple[iv] = ver

VERSION = tuple(vtuple)


def get_version(version=VERSION):
    assert len(version) == 5
    assert version[3] in ("alpha", "beta", "rc", "final")

    main = ".".join(str(x) for x in version[:3])
    sub = ""
    if version[3] != "final":
        mapping = {"alpha": "a", "beta": "b", "rc": "c"}
        sub = mapping[version[3]] + str(version[4])

    return main + sub
