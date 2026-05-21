with open("tests/test_bng_core.py", "r") as f:
    content = f.read()

content = content.replace("def test_bionetgen_plot():\n    argv = [", """def test_bionetgen_plot():
    import bionetgen as bng
    if not os.path.exists(os.path.join(*[tfold, "test"])):
        os.makedirs(os.path.join(*[tfold, "test"]))
    try:
        bng.run(os.path.join(*[tfold, "test.bngl"]), out=os.path.join(*[tfold, "test"]))
    except:
        pass
    argv = [""")

with open("tests/test_bng_core.py", "w") as f:
    f.write(content)

with open("tests/test_bionetgen.py", "r") as f:
    content = f.read()

content = content.replace("def test_bionetgen_plot():\n    argv = [", """def test_bionetgen_plot():
    import bionetgen as bng
    if not os.path.exists(os.path.join(*[tfold, "test"])):
        os.makedirs(os.path.join(*[tfold, "test"]))
    try:
        bng.run(os.path.join(*[tfold, "test.bngl"]), out=os.path.join(*[tfold, "test"]))
    except:
        pass
    argv = [""")

with open("tests/test_bionetgen.py", "w") as f:
    f.write(content)
