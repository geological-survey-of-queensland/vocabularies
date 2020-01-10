# Vocabulary Validation

Vocabulary validation is perfurmed using GSQ-created ontology rules formulated using the [SHACL constraint language](https://www.w3.org/TR/shacl/). The rules are given within files in this folder: `vocabulary-metadata.shape.ttl` etc.

There are several options for testing a given vocabulary with the relevant SHACL files but the main way is to use the [pySHACL tool](https://github.com/RDFLib/pySHACL) on the command line, something like this:

```
~$ pyshacl -s vocabulary-metadata.shape.ttl ../vocabularies/borehole-design.ttl
```
This command will check that the *Borehole Design* vocabulary, contained within the file `borehole-design.ttl` is validated against the *Vocabulary Metadata Shape* contained within the file `vocabulary-metadata.shape.ttl`.

For any given GSQ vocabulary, the relevant shapes are in this folder:

* *vocabulary-metadata.shape.ttl* - validates the vocabulary (`skos:conceptScheme`) metadata
* *concept.shape.ttl* - validates each `skos:Concept`s properties
* *agent.shape.ttl* - validates that any Agnet declarations (e.g. creators or publishers) are formulated correctly

Read the pySHACL documentation on how to install pySHACL or to use it online.
