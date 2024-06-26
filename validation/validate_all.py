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
voc_dir = Path(__file__).parent.parent / "vocabularies-gsq"
p = voc_dir.glob("*.ttl")
validity_state = {}

commands = [
    "report",
    "onebyone"
]

validators_dir = Path(__file__).parent

validators = [
    "vocpub",
    "vocpub-4.10",
    "gsq",
    "combined",
    "skosShapes.shapes",
]

if sys.argv[1] not in commands:
    print(f"You must supply a command to this script that is one of [{', '.join(commands)}]")
    exit(1)

if len(sys.argv) > 2:
    validator = sys.argv[2]
    if validator not in validators:
        print(f"If you indicate a validator, it must be one of [{', '.join(validators)}]. If you don't VocPub will be used")
        exit(1)
else:
    validator = "vocpub"

total_error_count = 0
if sys.argv[1] == "report":
    for f in sorted(p):
        print(f)
        try:
            v = validate(str(f), shacl_graph=f"{validator}.ttl")
            error_count = 0
            for s, o in v[1].subject_objects(predicate=URIRef("http://www.w3.org/ns/shacl#resultMessage")):
                error_count += 1
        except Exception as err:
            print(f"ERROR in {f}:", err)
            v = False,
            error_count = None
            
        if error_count > 0 or error_count is None:
            total_error_count += 1

        validity_state[f.name] = {
            "valid": v[0],
            "failures": error_count
        }

    with open(voc_dir / "validity.json", "w") as f:
        json.dump(validity_state, f, indent=4)

elif sys.argv[1] == "onebyone":
    print(f"Validating one by one in directory {voc_dir}")
    for f in sorted(p):
        print(f)
        try:
            v = validate(str(f), shacl_graph=f"{validators_dir / validator}.ttl", allow_warnings=True)
            if not v[0]:
                print("Invalid")
                print(v[2])
                exit()
            else:
                print("Valid")
        except Exception as e:
            print(e)
            exit()

print(f"Total errors:", total_error_count)

if total_error_count > 0:
    exit(1)
