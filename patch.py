with open(".github/workflows/ci.yml", "r") as f:
    text = f.read()

text = text.replace('os: [\'ubuntu-20.04\', \'windows-latest\', \'macos-latest\']', "os: ['ubuntu-latest', 'windows-latest', 'macos-latest']")

with open(".github/workflows/ci.yml", "w") as f:
    f.write(text)
