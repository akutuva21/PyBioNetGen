with open("setup.py", "r") as f:
    data = f.read()

data = data.replace('urllib.request.urlretrieve(bng_url, fname)', '''
    req = urllib.request.Request(bng_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(fname, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
''')

with open("setup.py", "w") as f:
    f.write(data)
