"""
This is a short script that just applies pySHACL to all the files in the vocabularies/ directory.

Its only dependency is pySHACL: pip install pyshacl

It is used like this:

~$ python validate_all.py COMMAND

Where COMMAND is one of "report" or "onebyone".

"report": validate all files and report result to a summary JSON file validity.json

"onebyone": validate files one-by-one and cease after a failure
"""
from pathlib import Path
from pyshacl import validate
from rdflib import URIRef
import json
import sys

# set this to the vocab folder
voc_dir = Path("../vocabularies-gsq")
p = voc_dir.glob("*.ttl")
validity_state = {}

commands = [
    "report",
    "onebyone"
]

validators = [
    "vocpub",
    "gsq",
    "combined"
]

if sys.argv[1] not in commands:
    print(f"You must supply a command to this script that is one of {', '.join(commands)}")
    exit()

if len(sys.argv) > 2:
    validator = sys.argv[2]
    if validator not in validators:
        print(f"If you indicate a validator, it must be one of  {', '.join(validators)}. If you don't VocPub will be used")
        exit()
else:
    validator = "vocpub"

if sys.argv[1] == "report":
    for f in sorted(p):
        print(f)
        try:
            v = validate(str(f), shacl_graph=f"{validator}.ttl")
            error_count = 0
            for s, o in v[1].subject_objects(predicate=URIRef("http://www.w3.org/ns/shacl#resultMessage")):
                error_count += 1
        except:
            print("ERROR")

        validity_state[f.name] = {
            "valid": v[0],
            "failures": error_count
        }

    with open(voc_dir / "validity.json", "w") as f:
        json.dump(validity_state, f, indent=4)

elif sys.argv[1] == "onebyone":
    for f in sorted(p):
        print(f)
        try:
            v = validate(str(f), shacl_graph=f"{validator}.ttl")
            if not v[0]:
                print("Invalid")
                print(v[2])
                exit()
            else:
                print("Valid")
        except:
            exit()