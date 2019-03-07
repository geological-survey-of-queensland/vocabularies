# GSQ Vocabularies
## Description
A collection of GSQ's vocabularies, formulated using SKOS, serialised as RDF (turtle) files as well as Python files for pushing these vocabularies into a GraphDB instance.

These are the source files for GSQ's vocabularies. The vocabularies appear online at their namespace locations which are given in their data, for example the vocab "GSQ Geophysical Surveys" has the following content:

```
...
<http://test.linked.data.gov.au/def/gsq-geophysical-survey> a owl:Ontology .

:conceptScheme a skos:ConceptScheme;
  dct:created "2019-02-06T10:44:40.696+10:00"^^xsd:dateTime;
  skos:prefLabel "GSQ Geophysical Surveys Keywords"@en .

:Data_Processing a skos:Concept;
  dct:created "2019-02-06T10:44:57.750+10:00"^^xsd:dateTime;
  skos:inScheme :conceptScheme;
  skos:prefLabel "Data Processing"@en;
skos:topConceptOf :conceptScheme .
...
```
... and it appears online at <http://test.linked.data.gov.au/def/gsq-geophysical-survey>.

Additionally, all GSQ vocabs and non-GSQ vocabs used by GSQ, are listed at <http://vocabs.gsq.cat>.


## Files
* **extra-\*.ttl** - background ontologies needed for vocab inferencing
* **gsq-\*.ttl** - GSQ vocab files
* **vocabs_load.py** - a Python script to load a GraphDB instance with the background ontologies and GSQ vocab files
* **vocabs_backup.py** - a Python script to dump a GrpahDB instance to GitHub
* **_config/** - configuration info for the Python files. **template.py** contains all the variables but wuth junk values. Copy this to __init__.py and correct values for use
* **repo-config.ttl.template** - a GraphDB repository RDF template to be used to create a 'vocabs' repository 

## License
This code repository's content are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), the deed of which is stored in this repository here: [LICENSE](LICENSE).


## Contacts
*Vocabularies owner*:  
**Mark Gordon**  
Geological Survey of Quensland  
Department of Natural Resources, Mines and Energy  
Brisbane, QLD, Australia  
<mark.gordon@dnrme.qld.gov.au>  


*Vocabulary collector*:  
**Sophie Darnell**  
CSIRO Land & Water, Brisbane, Australia    
<sophie.darnell@csiro.au>  


*Technical contact*:  
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water, Brisbane, Australia    
<nicholas.car@csiro.au>  
<http://orcid.org/0000-0002-8742-7730>  
