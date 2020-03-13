# Scripts to deploy TTL files to GraphDB

These scripts loads all of the vocabulary TTL files from the Github repository at https://github.com/geological-survey-of-queensland/vocabularies into GraphDB.

## vocabs_load.py

The script **vocabs_load.py** loads all of the vocabulary TTL files from the Github repository into GraphDB.

## config-template-xxx.py

Edit the relevant config file, test or production, with GraphDB and Github account credentials. Rename to **config.py**

The **vocabs_load.py** file uses the **config.py** file for its configuration.
