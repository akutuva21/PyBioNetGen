def replace(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    old = """app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]
def_bng_path = conf["bngpath"]"""

    new = """from bionetgen.core.defaults import BNGDefaults
d = BNGDefaults()
def_bng_path = d.bng_path"""

    if old in content:
        content = content.replace(old, new)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Replaced in {filepath}")

replace("bionetgen/modelapi/bngfile.py")
replace("bionetgen/network/networkparser.py")

def replace2(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    old = """app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]"""

    new = """from bionetgen.core.defaults import BNGDefaults
d = BNGDefaults()
conf = {"bngpath": d.bng_path}"""

    if old in content:
        content = content.replace(old, new)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Replaced in {filepath}")

replace2("bionetgen/modelapi/runner.py")
