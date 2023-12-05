from os.path import join, dirname
import os
import glob
from pathlib import Path
from rdflib import Graph
from rdflib.namespace import RDF, SKOS
import pickle

VOCABS_DIR = Path(__file__).parent.parent.resolve().glob("vocabularies-*/*.ttl")
VOCABS_PICKLE = Path(__file__).parent / "all_vocabs.pickle"

if Path(VOCABS_PICKLE).is_file():
    print("reading all vocabs from pickle file")
    with open(VOCABS_PICKLE, "rb") as f:
        g = pickle.load(f)
else:
    print("no pickle file so creating it from RDF source files")
    g = Graph()
    for vocab in VOCABS_DIR:
        print(f"parsing {vocab}")
        g.parse(vocab)
        print(len(g))
    print(f"pickleing all vocabs to {VOCABS_PICKLE}")
    pickle.dump(g, VOCABS_PICKLE.open("wb"))

print(len(g))

q = """
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX themes: <https://linked.data.gov.au/def/fsdf/themes/>
 
    SELECT ?cs ?theme
    WHERE {
        ?cs a skos:ConceptScheme ;
            dcat:theme ?theme ;
        .
        
        VALUES ?theme {
            themes:buildings-and-settlements
            themes:geocoded-addressing
            themes:place-names
            themes:positioning
            themes:spatial
            themes:transport
        }
    }
    ORDER BY ?theme ?cs
    """
for r in g.query(q):
    print(f'{r["cs"]}: {r["theme"]}')
