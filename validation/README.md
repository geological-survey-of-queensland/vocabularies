# Vocabulary Validation

GSQ vocabs must be valid according to the [VocPub Profile](https://w3id.org/profile/vocbpub) which is a specification that constrains SKOS to ensure that certain vocab element properties are present, such as definitions for `Concept` instances, basic `ConceptScheme` metadata etc. 

In addition to all the rules imposed by VocPub and, through inheritance SKOS, GSQ vocabs must also be valid according to rules within the _GSQ Profile of VocPub_ which simply adds a few more GSQ-specific vocab tests. 

## Validators

Vocabulary validation is performed technically using graph pattern matching data objects called _shapes_. These are like a template of content that must be present or configured in a particular way in order for the vocabulary to be valid according to some specification.

VocPub provides a validator written in the [SHACL constraint language](https://www.w3.org/TR/shacl/) which can be downloaded here:

* <https://w3id.org/profile/vocbpub/validator>

A working copy of it is stored in this directory as `vocpub.ttl` too.

The extended GSQ validator is stored in this directory as `gsq.ttl`.

A further validator, `gsq-compounded.ttl`, is a combined validator including the _GSQ Profile of VocPub_'s validator, the `VocPub Profile` validator and a SKOS validator all in one. It is all you really need to validate GSQ vocabs with. 

## Validating

To use those GSQ and other validators, you need a SHACL engine that can apply the validator file to a target data file. Here are options for doing that.

### Online
You can use the [RDF Tool](http://rdftools.kurrawong.net/validators) to validate RDF data online. It comes pre-loaded with many validators and you can also add your own in too. Just select your validator, or upload / copy 'n paste it, and your data file in the same way and hit validate.

It will be updated soon with this new VocPub validator version and with the GSQ validator.

### Command line
Use the Python [pySHACL tool](https://github.com/RDFLib/pySHACL) which is the basis for the RDF Tools validation service above, on the command line, something like this:

```
~$ pyshacl -s vocpub.ttl ../vocabularies/borehole-design.ttl
```

`-s` indicates the _shapes_ validator file and `../vocabularies/borehole-design.ttl` is the vocab under test.

Any validation errors will be printed to screen.

### Bulk validation
All vocabs can be validated at once using the bulk validator Python script `validate_all.py` which uses pySHACL. Run it like this:

```
python validate_all.py report
```
