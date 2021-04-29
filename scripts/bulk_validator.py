from pathlib import Path
from pyshacl import validate
from rdflib import URIRef
import json

# set this to the vocab folder
p = Path("../vocabularies").glob("*.ttl")

validity_state = {}
for f in p:
    print(f)
    try:
        v = validate(str(f), shacl_graph="validator.shacl.ttl")  # file from https://w3id.org/profile/vocpub/validator
        error_count = 0
        for s, o in v[1].subject_objects(predicate=URIRef("http://www.w3.org/ns/shacl#resultMessage")):
            error_count += 1
    except:
        print("ERROR")

    validity_state[f.name] = {
        "valid": v[0],
        "failures": error_count
    }

with open("../vocabularies/validity.json", "w") as f:
    json.dump(validity_state, f, indent=4)

