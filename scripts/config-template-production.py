# Configuration file for vocabs_load.py file. Edit this template and save as config.py

GRAPHDB_REPO_ID = 'GSQ_Vocabularies_Master' 
GRAPHDB_REPO_URI = 'https://graphdb.gsq.digital/repositories/{}'.format(GRAPHDB_REPO_ID) 
GRAPHDB_LOAD_DATA_URI = 'https://graphdb.gsq.digital/rest/data/import/upload/{}/url'.format(GRAPHDB_REPO_ID) 
GRAPHDB_USR = 'graphdb_username'
GRAPHDB_PWD = 'graphdb_password'

GITHUB_RAW_URI_BASE = 'https://raw.githubusercontent.com/geological-survey-of-queensland/vocabularies/master/vocabularies/'

GITHUB_USR = 'github_username'  # or any valid GitHub account
GITHUB_PWD = 'github_password'  # for the valid GitHub account
