import requests
import json
from github import Github, GithubException
import base64
from rdflib import Graph
from scripts import config


def load_one_vocab_from_github(vocab_file_name, base_url, pref_label):
    """Loads a turtle file of RDF from GitHub into a Named Graph (context) in GraphDB

    :param vocab_file_name: the name of the file in the vocabularies folder in GitHub
    :param base_url: the context URI (Named Graph URI) for the vocab
    :param pref_label: the preferred label of the vocabulary
    :return:
    """
    namespace = base_url + '/'
    r = requests.post(
        config.GRAPHDB_LOAD_DATA_URI,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': namespace,
            'context': base_url,
            'data': config.GITHUB_RAW_URI_BASE + vocab_file_name,
            'forceSerial': True,
            'format': 'text/turtle',
            'message': '',
            'name': pref_label,
            'parserSettings': {
                'failOnUnknownDataTypes': True,
                'failOnUnknownLanguageTags': True,
                'normalizeDataTypeValues': True,
                'normalizeLanguageTags': True,
                'preserveBNodeIds': True,
                'stopOnError': True,
                'verifyDataTypeValues': True,
                'verifyLanguageTags': True,
                'verifyRelativeURIs': True,
                'verifyURISyntax': True
            },
            'replaceGraphs': [
                base_url  # same as Context
            ],
            'status': 'PENDING',
            'timestamp': 0,
            'type': 'string',
            'xRequestIdHeaders': 'string'
        }
    )

    if r.status_code != 201:
        return str(r.status_code) + "\n" + r.content.decode('utf-8')
    return "loaded"


# not used now
def load_all_background_onts_from_github():
    print('Loading background ontologies from GitHub')
    background_onts = [
        {
            'name': 'RDF Ontology',
            'namespace': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'file': 'rdf.ttl'
        },
        {
            'name': 'RDFS Ontology',
            'namespace': 'http://www.w3.org/2000/01/rdf-schema#',
            'file': 'rdfs.ttl'
        },
        {
            'name': 'OWL Ontology',
            'namespace': 'http://www.w3.org/2002/07/owl#',
            'file': 'owl.ttl'
        },
        {
            'name': 'SKOS Ontology',
            'namespace': 'http://www.w3.org/2004/02/skos/core#',
            'file': 'skos.ttl'
        },
    ]

    for ont in background_onts:
        print('Loading {}'.format(ont['name']))
        r = requests.post(
            config.GRAPHDB_LOAD_DATA_URI,
            auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'text/plain'
            },
            json={
                'baseURI': ont['namespace'],
                'context': ont['namespace'],
                'data': config.GITHUB_RAW_URI_BASE + 'ontologies/' + ont['file'],
                'forceSerial': True,
                'format': 'text/turtle',
                'message': '',
                'name': ont['name'],
                'parserSettings': {
                    'failOnUnknownDataTypes': True,
                    'failOnUnknownLanguageTags': True,
                    'normalizeDataTypeValues': True,
                    'normalizeLanguageTags': True,
                    'preserveBNodeIds': True,
                    'stopOnError': True,
                    'verifyDataTypeValues': True,
                    'verifyLanguageTags': True,
                    'verifyRelativeURIs': True,
                    'verifyURISyntax': True
                },
                'replaceGraphs': [
                    ont['namespace']  # same as Context
                ],
                'status': 'PENDING',
                'timestamp': 0,
                'type': 'string',
                'xRequestIdHeaders': 'string'
            }
        )

        if r.status_code != 202:
            print(r.content.decode('utf-8'))
            return r.status_code
        else:
            print('Loaded ' + ont['name'])

    return True


def load_all_vocabs_details_from_github():
    """Uses the GitHub API via the Python client to get all the vocab details from the files in
    the vocabularies/ folder

    :return: a dict of vocabularies' details
    """
    print('Loading all vocabs from GitHub')
    print("Vocabs to be uploaded:")
    if config.GITHUB_USR:
        print("Using passwords will be deprecated in Nov 2020, try to use a personal token instead")
        gh = Github(config.GITHUB_USR, config.GITHUB_PWD)
    else:
        gh = Github(config.GITHUB_TOKEN)
    repo = gh.get_repo("geological-survey-of-queensland/vocabularies")
    contents = repo.get_contents("vocabularies")
    c = 0
    for content_file in contents:
        fn = content_file.path.replace("vocabularies/", "")
        if fn.endswith(".ttl"):
            print(" - " + fn)
            c += 1
    print("\n{} vocabs in total".format(c))

    vocabs = {}
    for content_file in contents:
        fn = content_file.path.replace("vocabularies/", "")
        if fn.endswith(".ttl"):
            print("Reading {}".format(fn))
            try:
                fc = repo.get_contents("vocabularies/" + fn)
            except GithubException as e:
                for err in e.data.get('errors'):
                    if err['code'] == 'too_large':
                        print("File is above 1MB, using Data API call")
                        fc = repo.get_git_blob(content_file.sha)

            data = base64.b64decode(fc.content).decode('utf-8')
            g = Graph().parse(data=data, format="turtle")
            q = '''
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?uri ?pl
                WHERE {
                    ?uri a owl:Ontology ;
                        skos:prefLabel ?pl .
                }
            '''
            if not g.query(q):
                print("There was an error parsing or querying the graph. " 
                      "Ensure it contains 'a owl:Ontology' and 'skos:prefLabel'")

            for r in g.query(q):
                vocabs[fn] = {
                    "context_uri": str(r["uri"]),
                    "pref_label": str(r["pl"]),
                    "github_raw_uri": config.GITHUB_RAW_URI_BASE + fn
                }

    return vocabs


# not used
def list_repositories():
    r = requests.get(
        config.GRAPHDB_REPO_URI,
        headers={'Accept': 'application/json'},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return r.json


# not used
def delete_repo():
    r = requests.delete(
        config.GRAPHDB_REPO_URI,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    if r.status_code == 200:
        print('Deleted repo {}'.format(config.GRAPHDB_REPO_ID))
    else:
        print('ERROR: did not delete repo {}, message: {}'.format(config.GRAPHDB_REPO_ID, r.text))


def purge_repo():
    """Deletes (purges) all the triples from the repo given in config

    :return: print ut of "ok" or error text
    """
    print("Purging repo {}".format(config.GRAPHDB_REPO_ID))
    r = requests.delete(
        config.GRAPHDB_REPO_URI + "/statements",
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={"Accept": "application/json"}
    )
    if r.ok:
        print("OK - deleted all statements")
    else:
        print(r.text)


# not used
def make_repo_config_file(template_file, base_url, repo_id, repo_label):
    with open(template_file, 'r') as f:
        config_template_contents = f.read()
        return config_template_contents\
                    .replace('{repo_id}', repo_id)\
                    .replace('{repo_label}', repo_label)\
                    .replace('{base_url}', base_url)


# not used
def create_repo(repo_config):
    r = requests.post(
        config.GRAPHDB_REPO_URI,
        files={'config': ('config.ttl', repo_config)},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    if r.status_code == 201:
        print('Created repo {}'.format(config.GRAPHDB_REPO_ID))
    else:
        print('ERROR: did not create repo {}, message: {}'.format(config.GRAPHDB_REPO_ID, r.text))


if __name__ == '__main__':
    # purge the repo
    purge_repo()

    # generate vocab index from GitHub
    VOCABS = load_all_vocabs_details_from_github()

    # Load all vocabs
    for file_name, details in VOCABS.items():
        print("Loading {}".format(file_name))
        x = load_one_vocab_from_github(
            file_name,
            details['context_uri'],
            details["pref_label"]
        )
        print(x)
