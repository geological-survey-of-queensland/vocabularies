# Vocabulary Validation

Vocabulary validation is performed using the [VocPub Profile](https://w3id.org/profile/vocbpub) which is a specification that constrains SKOS to ensure that certain properties are presente for vocab elements, such as definitions for `Concept` instances. VocPub provides a validator written in the [SHACL constraint language](https://www.w3.org/TR/shacl/) which can be downloaded here:

* <https://w3id.org/profile/vocbpub/validator>

## How to validate
### Command line
There are several options for testing a given vocabulary with the VocPub validator but the main way is to use the [pySHACL tool](https://github.com/RDFLib/pySHACL) on the command line, something like this:

```
~$ pyshacl -s validator.shacl.ttl ../vocabularies/borehole-design.ttl
```
This command will check that the *Borehole Design* vocabulary, contained within the file `borehole-design.ttl` is validated VocPub constraints and will print any errors.

### Bulk validaton
All vocabs can be validated using the Bulk Validator script in `scritps/` too.

### SHACL Playground
The validator file and any target vocab can be copied into the [SHACL Playground](https://shacl.org/playground/) online tool and validated there.
