# GSQ Vocabularies
## Description
A collection of GSQ's vocabularies, formulated using SKOS, seriealised as RDF (turtle) files.

These are the source files for GSQ's vocabularies. The vocabularies appear online at their namespace locations which are given in their data, for example the vocab "GSQ Geophysical Surveys" has the following content:

```
...
<http://test.linked.data.gov.au/def/gsq-geophysical-survey> a owl:Ontology .

:ConceptScheme a skos:ConceptScheme;
  dct:created "2019-02-06T10:44:40.696+10:00"^^xsd:dateTime;
  skos:prefLabel "GSQ Geophysical Surveys Keywords"@en .

:Data_Processing a skos:Concept;
  dct:created "2019-02-06T10:44:57.750+10:00"^^xsd:dateTime;
  skos:inScheme :ConceptScheme;
  skos:prefLabel "Data Processing"@en;
skos:topConceptOf :ConceptScheme .
...
```
... and it appears online at <http://test.linked.data.gov.au/def/gsq-geophysical-survey>.

Additionally, all GSQ vocabs and non-GSQ vocabs used by GSQ, are listed at <http://vocabs.gsq.cat>.


## License
This code repository's content are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), the deed of which is stored in this repository here: [LICENSE](LICENSE).


## Contacts
*Vocabularies owner*:  
**David Crosswell**  
Geological Survey of Quensland  
Department of Natural Resources, Mines and Energy  
Brisbane, QLD, Australia  
<david.crosswell@dnrme.qld.gov.au>  


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
