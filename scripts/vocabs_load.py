import requests
import json
import os
import rdflib
from scripts import config


# create-repos or load-data
def load_one_vocab_from_github(repo_id, vocab_id, base_url, label):
    namespace = base_url + '/'
    r = requests.post(
        config.GRAPHDB_LOAD_DATA_URI.format(repo_id),
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': namespace,
            'context': namespace,
            'data': config.GITHUB_RAW_URI_BASE + vocab_id + '.ttl',
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
        print(r.content.decode('utf-8'))
    return r.status_code


def load_all_background_onts_from_github(repo_id):
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
        print('repo: {}'.format(repo_id))
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


def load_all_vocabs_from_github(repo_id):
    for file in os.listdir('.'):
        if file.startswith('gsq-') and file.endswith('.ttl'):
            g = rdflib.Graph().parse(file, format='turtle')

            q = '''
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?uri ?pl
                WHERE {
                    ?uri a owl:Ontology .
                    ?uri2 a skos:ConceptScheme ;
                        skos:prefLabel ?name .
                }
            '''
            for r in g.query(q):
                vocab_id = r['uri'].split('/')[-1]
                base_url = r['uri']
                name = r['pl']

                print('{} {} {}'.format(vocab_id, base_url, name))
                #load_one_vocab_from_github(repo_id, vocab_id, base_url, label)


def list_repositories():
    r = requests.get(
        config.GRAPHDB_REPOS_URI,
        headers={'Accept': 'application/json'},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return json.loads(r.content.decode('utf-8'))


def delete_repo(repo_id):
    r = requests.delete(
        config.GRAPHDB_REPOS_URI + '/' + repo_id,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    if r.status_code == 200:
        print('Deleted repo {}'.format(repo_id))
    else:
        print('ERROR: did not delete repo {}, message: {}'.format(repo_id, r.text))


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
    repo_id = 'GSQ_Vocabularies_core'
    repo_name = 'GSQ Vocabularies'

    # delete_repo(repo_id)
    #
    # repo_config = make_repo_config_file(
    #     'repo-config.ttl.template',
    #     'http://linked.data.gov.au/def/',
    #     repo_id,
    #     repo_name
    # )

    # # load_all_vocabs_from_github()
    load_all_background_onts_from_github(repo_id)
