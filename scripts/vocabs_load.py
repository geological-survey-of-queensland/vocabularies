import requests
import json
from github import Github
import base64
import os
from rdflib import Graph
from scripts import config


# create-repos or load-data
def load_one_vocab_from_github(repo_id, vocab_file_name, base_url, label):
    namespace = base_url + '/'
    r = requests.post(
        config.GRAPHDB_LOAD_DATA_URI.format(repo_id),
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': namespace,
            'context': base_url,
            'data': config.GITHUB_RAW_URI_BASE + vocab_file_name,
            'forceSerial': True,
            'format': 'text/turtle',
            'message': '',
            'name': label,
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


def load_all_background_onts_from_github(repo_id):
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
            config.GRAPHDB_LOAD_DATA_URI.format(repo_id),
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
    print('Loading all vocabs from GitHub')
    print("Vocabs to be uploaded:")
    gh = Github(config.GITHUB_USR, config.GITHUB_PWD)
    repo = gh.get_repo("geological-survey-of-queensland/vocabularies")
    contents = repo.get_contents("vocabularies")
    c = 0
    for content_file in contents:
        fn = content_file.path.replace("vocabularies/", "")
        if fn.endswith(".ttl"):
            print(" - " + fn)
            c += 1
    print("\n{} vocabs in total".format(c))

    VOCABS = {}
    for content_file in contents:
        fn = content_file.path.replace("vocabularies/", "")
        if fn.endswith(".ttl"):
            if fn == "minerals.ttl":
                print("Skipping minerals as too large")
            else:
                print("Reading {}".format(fn))
                fc = repo.get_contents("vocabularies/" + fn)
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
                for r in g.query(q):
                    VOCABS[fn] = {
                        "context_uri": str(r["uri"]),
                        "pref_label": str(r["pl"]),
                        "github_raw_uri": config.GITHUB_RAW_URI_BASE + fn
                    }

    return VOCABS


def list_repositories():
    r = requests.get(
        config.GRAPHDB_REPOS_URI,
        headers={'Accept': 'application/json'},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return json.loads(r.content.decode('utf-8'))


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
    # clear repo of all vocabs
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


def make_repo_config_file(template_file, base_url, repo_id, repo_label):
    with open(template_file, 'r') as f:
        config_template_contents = f.read()
        return config_template_contents\
                    .replace('{repo_id}', repo_id)\
                    .replace('{repo_label}', repo_label)\
                    .replace('{base_url}', base_url)


def create_repo(repo_config):
    r = requests.post(
        config.GRAPHDB_REPOS_URI,
        files={'config': ('config.ttl', repo_config)},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    if r.status_code == 201:
        print('Created repo {}'.format(repo_id))
    else:
        print('ERROR: did not create repo {}, message: {}'.format(repo_id, r.text))


if __name__ == '__main__':
    # generate vocab index from GitHub
    VOCABS = load_all_vocabs_details_from_github()

    # Load all vocabs
    for file_name, details in VOCABS.items():
        print("Loading {}".format(file_name))
        x = load_one_vocab_from_github(
            config.GRAPHDB_REPO_ID,
            file_name,
            details['context_uri'],
            details["pref_label"]
        )
        print(x)
