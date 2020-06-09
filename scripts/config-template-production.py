# Configuration file for vocabs_load.py file. Edit this template and save as config.py

GRAPHDB_REPO_ID = 'vocabs'
GRAPHDB_REPO_URI = 'http://localhost:7200/repositories/{}'.format(GRAPHDB_REPO_ID)
GRAPHDB_LOAD_DATA_URI = 'http://localhost:7200/rest/data/import/upload/{}/url'.format(GRAPHDB_REPO_ID)
GRAPHDB_USR = ''
GRAPHDB_PWD = ''

GITHUB_RAW_URI_BASE = 'https://raw.githubusercontent.com/geological-survey-of-queensland/vocabularies/master/vocabularies/'

GITHUB_USR = 'github_username'  # or any valid GitHub account
GITHUB_PWD = 'github_password'  # for the valid GitHub account
GITHUB_TOKEN = 'github_personal_access_token' # recommended for use from 2020, not user/pass
