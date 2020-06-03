# This script can apply pySHACL validation to each vocab in /vocabularies
#
# Current configuration excludes the Gregorian Calendar months from Concept validation since it has multiple prefLabels
# in multiple languages our SHACL files can't handle

import os
from os.path import join, dirname
import glob
from rdflib import Graph
import pyshacl


vocabs_dir = join(dirname(os.getcwd()), "vocabularies")
shapes_dir = join(dirname(os.getcwd()), "shapes")
conceptscheme_shape_graph = Graph().parse(join(shapes_dir, "vocabulary-metadata.shape.ttl"), format="turtle")
concept_shape_graph = Graph().parse(join(shapes_dir, "concept.shape.ttl"), format="turtle")
agent_shape_graph = Graph().parse(join(shapes_dir, "agent.shape.ttl"), format="turtle")

for v in sorted(glob.glob(vocabs_dir + "/*.ttl")):
    print("validating: {}".format(v))

    conforms, results_graph, results_text = pyshacl.validate(
        Graph().parse(v, format="turtle"),
        shacl_graph=conceptscheme_shape_graph
    )
    if not conforms:
        print(results_text)
        exit()

    if "gregorian" not in v:
        conforms, results_graph, results_text = pyshacl.validate(
            Graph().parse(v, format="turtle"),
            shacl_graph=concept_shape_graph
        )
        if not conforms:
            print(results_text)
            exit()

    conforms, results_graph, results_text = pyshacl.validate(
        Graph().parse(v, format="turtle"),
        shacl_graph=agent_shape_graph
    )
    if not conforms:
        print(results_text)
        exit()
