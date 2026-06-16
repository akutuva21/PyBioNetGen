import re, sys

filepath = sys.argv[1]
with open(filepath, "r") as f:
    content = f.read()


# Pattern: <<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> origin/main
# Keep both sides separated by a blank line
def replace_conflict(m):
    head = m.group(1).strip()
    main = m.group(2).strip()
    return head + "\n\n\n" + main


content = re.sub(
    r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> origin/main",
    replace_conflict,
    content,
    flags=re.DOTALL,
)

# Clean up any remaining orphan conflict markers
content = content.replace(">>>>>>> origin/main", "")
content = content.replace("<<<<<<< HEAD", "")
content = content.replace("=======", "")

with open(filepath, "w") as f:
    f.write(content)

print("Resolved conflicts in", filepath)
