# Scripts to import TTL files to GraphDB

These scripts imports all of the vocabulary TTL files from the Github repository at https://github.com/geological-survey-of-queensland/vocabularies into GraphDB.

## vocabs_load.py

Run the script **vocabs_load.py** to import all of the vocabulary TTL files from the Github repository into GraphDB.

## config-template-xxx.py

Edit the relevant config file, test or production, with GraphDB and Github account credentials. Rename to **config.py**

The **vocabs_load.py** file uses the **config.py** file for its configuration.

## Manually load vocabs that script doesn't load

NOTE: The current script will not load the file **minerals.ttl** as it exceeds 2MB (this needs to be fixed).  
NOTE: The current script will not load the file **qudt-uom.ttl** due to a bug in the load script (this needs to be fixed).

Until these issue are resolved, the **minerals.ttl** and **qudt-uom.ttl** files must be manually imported through the GraphDB administration interface - see instructions below.

## How to manually import TTL files

See https://github.com/geological-survey-of-queensland/vocabularies/wiki/GraphDB-manual-import-of-TTL-files

## Refresh the VocPrez cache

To refresh the VocPrez cache of vocabularies, restart **Apache httpd** on the VocPrez EC2 instance.
