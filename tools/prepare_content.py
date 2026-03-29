import base64
import sys

inp = open(sys.argv[1]).read()

# normalize
inp = inp.replace("\r\n", "\n")
inp = inp.replace("\t", "  ")
inp = "\n".join(line.rstrip() for line in inp.splitlines())

if not inp.endswith("\n"):
    inp += "\n"

# encode
encoded = base64.b64encode(inp.encode()).decode()

open(sys.argv[2], "w").write(encoded)
