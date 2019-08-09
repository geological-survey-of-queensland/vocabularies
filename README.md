# GSQ Vocabularies
## Introduction
The Geological Survey of Queensland (GSQ) publishes vocabularies - a way to describe things and the relationship between things.

A vocabulary is a set of agreed terms:
* In GSQ, a vocabulary defines the terms used to describe and represent things in the domain of science and data management.
* Vocabularies align information within a business area or across systems.
* Vocabularies can be very complex (with thousands of terms) or very simple (describing one or two concepts only).


## Vocabulary - how it all hangs together
<img src="vocabulary_context_diagram.png" style="width:800px;" alt="Vocabulary context diagram" />  

**Fig. 1: Vocabulary context diagram**

1. We use tools such as Vocbench or Excel to create the vocabulary using [SKOS Simple Knowledge Organization System](https://www.w3.org/TR/skos-reference). See also the [SKOS Primer](https://www.w3.org/TR/skos-primer) for the basics.
2. The native format for a vocabulary is a TTL (turtle) file. This file contains [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) triples - subject > predicate > object statements.
3. We use Github (where you are now) to store and manage versions of vocabulary TTL files. Github also provides workflow functionality to approve vocabularies. Read the getting started guide https://guides.github.com/activities/hello-world/
4. We import the TTL files into GraphDB to create a triple store. GraphDB lets us query the triples.
5. VocPrez presents our vocabs on the web for people and computers to read. VocPrez pulls the triples from GraphDB to create a cache of the vocabularies.
6. CKAN drop-down form fields pull their values from VocPrez. This ensures that the attributes uses to describe a dataset comes from the controlled vocabulary. 


## How to create a vocabulary
<img src="vocabulary-build-pull-workflow.png" style="width:100%;" alt="Vocabulary build and pull process" />  

**Fig. 2: Vocabulary build and pull process**

1. Select the vocabulary editor of your choice.
2. Create the vocabulary using the [SKOS Simple Knowledge Organization System](https://www.w3.org/TR/skos-reference/). See also the [SKOS Primer] for the basics(https://www.w3.org/TR/skos-primer/). NOTE: Always first check if there is an international or national vocabulary (see below for links).
  a. Use [Vocbench](www.vocbench.gsq.digital:7200/) to create the vocabulary.
  b. Use the Excel template to create the vocabulary. *(Vance can you upload the template to this repository and put the link here)*
  c. Edit the vocab TTL file in Visual Studio Code. Use the extension [Language Support for RDF related language syntax](https://marketplace.visualstudio.com/items?itemName=fantasticfears.semantic-data-model-language) for formatting support.
3. Export the vocabulary to a TTL file. If using Vocbench, it is easier to export the TTL from the Build repository in GraphDB. Follow the [instructions here](http://graphdb.ontotext.com/documentation/standard/exporting-data.html).
4. Validate the TTL file using the [online Skosify tool](http://demo.seco.tkk.fi/skosify/skosify). Tick the checkboxes *Keep skos:related relationships within the same hierarchy* and *Include skos:narrower relations in output*
5. Import the TTL file into a development branch in Github. Name your branch *dev-yourGithubusername*. See [how-to instructions here](https://guides.github.com/activities/hello-world/).
6. When you're ready to publish your vocabulary into Test, submit a Pull Request to the TEST branch. See [how-to instructions here](https://guides.github.com/activities/hello-world/#pr).
7. A member of the Data Integrity Team will review your vocabulary and either Approve or Request Changes. See [how-to instructions here](https://help.github.com/en/articles/approving-a-pull-request-with-required-reviews).
8. If the pull request is approved, the vocab will now be in the TEST branch.


## How to publish a vocabulary to VocPrez Test
1. Import the vocabulary TTL file into the Core Repository in the Test Graph DB https://test.graphdb.gsq.digital using the [instructions here](http://graphdb.ontotext.com/documentation/standard/loading-data-using-the-workbench.html).
2. Restart the Test VocPrez to refresh the VocPrez cache (we will automate this step).
3. The vocabulary is now published in the Test VocPrez at https://test.vocabs.gsq.digital


## How to publish a vocabulary to VocPrez Production
1. Verify that the URI of the vocabulary is valid and does not collide with an existing URI. URIs are in the format  http://linked.data.gov.au/def/vocabulary-name
2. If not already done, register the URI of the vocabulary through the console at http://linked.data.gov.au (John K to add process steps here). The registration is reviewed and approved by the managers of the Linked Data Working Group.
3. Perform a Pull Request from the TEST branch in Github to the MASTER branch.
4. A member of the Data Integrity Team will review your vocabulary and either Approve or Request Changes.
5. Import the vocabulary TTL file into the Core Repository in the Production Graph DB https://graphdb.gsq.digital using the [instructions here](http://graphdb.ontotext.com/documentation/standard/loading-data-using-the-workbench.html).
6. Restart the Production VocPrez to refresh the VocPrez cache (we will automate this step).
7. The vocabulary is now published in the Production VocPrez at https://vocabs.gsq.digital. Please note that the vocab will not display in VocPrez until the URI registration at http://linked.data.gov.au is approved. 


## Files
* **ontologies/\*.ttl** - background ontologies needed for vocab inferencing
* **gsq-\*.ttl** - GSQ vocab files
* **vocabs_load.py** - a Python script to load a GraphDB instance with the background ontologies and GSQ vocab files
* **scripts/** - Python scripts to dump/load a GrpahDB instance with these vocab files


## License
This code repository's content are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), the deed of which is stored in this repository here: [LICENSE](LICENSE).


## Contacts
*Vocabularies owner*:  
**Mark Gordon**  
Geological Survey of Quensland  
Department of Natural Resources, Mines and Energy  
Brisbane, QLD, Australia  
<mark.gordon@dnrme.qld.gov.au>  

*Technical contact*:  
**Vance Kelly**  
Geological Survey of Quensland  
Department of Natural Resources, Mines and Energy  
Brisbane, QLD, Australia    
<vance.kelly@dnrme.qld.gov.au>  
