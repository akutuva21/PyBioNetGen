import urllib.request
req = urllib.request.Request('https://github.com/RuleWorld/bionetgen/releases/download/BioNetGen-2.9.3/BioNetGen-2.9.3-linux.tar.gz', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response, open('bng.gz', 'wb') as out_file:
    out_file.write(response.read())
