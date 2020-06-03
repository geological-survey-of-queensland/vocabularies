# This script checks the redirect status of vocabs' URIs
#
# as of 2020-06-03, all 64 vocab' URIs are resulting in successful redirects to GSQ VocPrez

import requests
import os
from os.path import join, dirname
import glob
from rdflib import Graph
from rdflib.namespace import RDF, SKOS


def get_vocab_uri_statuses():
    vocabs_dir = join(dirname(os.getcwd()), "vocabularies")
    vocab_uris = []
    for v in sorted(glob.glob(vocabs_dir + "/*.ttl")):
        g = Graph().parse(v, format="turtle")
        for s, p, o in g.triples((None, RDF.type, SKOS.ConceptScheme)):
            vocab_uris.append(str(s).replace("http", "https"))

    vocab_uri_statues = []
    for vocab_uri in vocab_uris:
        r = requests.head(vocab_uri)
        if r.status_code == 401:
            print(vocab_uri)
        status = r.status_code
        vocab_uri_statues.append((vocab_uri, status))

    return vocab_uri_statues


if __name__ == "__main__":
    vocab_uri_statuses = get_vocab_uri_statuses()
    resolving = 0
    unresolving = 0
    total = len(vocab_uri_statuses)

    for r in vocab_uri_statuses:
        if r[1] == 404:
            unresolving += 1
            print(r[0])
        elif r[1] in [302, 200]:  # the only 200 is the W3C's Gregorian (months) vocab
            resolving += 1

    print("resolving: {}".format(resolving))
    print("unresolving: {}".format(unresolving))
    print("total: {}".format(total))
