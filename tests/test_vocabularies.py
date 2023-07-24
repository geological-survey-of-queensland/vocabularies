from pathlib import Path

import pytest
import pyshacl
from rdflib import Graph


@pytest.fixture
def vocpub_graph() -> Graph:
    graph = Graph()
    graph.parse(Path("validation/vocpub.ttl"))
    return graph


def _get_vocab_files():
    directories = Path(".").glob("./vocabularies-*")
    files = []
    for directory in directories:
        files += directory.glob("**/*.ttl")

    return files


@pytest.mark.parametrize("file", _get_vocab_files())
def test_vocabs(file: Path, vocpub_graph: Graph):
    conforms, _, results_text = pyshacl.validate(
        data_graph=Graph().parse(file),
        shacl_graph=vocpub_graph,
        allow_warnings=True,
    )

    assert conforms, f"{file} failed:\n{results_text}"
