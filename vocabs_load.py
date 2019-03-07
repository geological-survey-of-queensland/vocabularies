import requests
import json
import os
import rdflib

import _config as config


# create-repos or load-data
def load_one_vocab_from_github(vocab_id, base_url, label):
    # load the vocab
    r = requests.post(
        config.GRAPHDB_LOAD_DATA_URI,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': base_url,
            'context': base_url,
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


def load_all_background_onts_from_github():
    background_onts = [
        {
            'label': 'RDF Ontology',
            'namespace': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        },
        {
            'label': 'RDFS Ontology',
            'namespace': 'http://www.w3.org/2000/01/rdf-schema#'
        },
        {
            'label': 'OWL Ontology',
            'namespace': 'http://www.w3.org/2002/07/owl#'
        },
        {
            'label': 'SKOS Ontology',
            'namespace': 'http://www.w3.org/2004/02/skos/core#'
        },
    ]

    for ont in background_onts:
        r = requests.post(
            config.GRAPHDB_LOAD_DATA_URI,
            auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            json={
                'baseURI': ont['namespace'],
                'context': ont['namespace'],
                'data': config.GITHUB_RAW_URI_BASE + 'extra-rdf.ttl',
                'forceSerial': True,
                'format': 'text/turtle',
                'message': '',
                'name': ont['label'],
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
            print('Loaded ' + ont['label'])

    return True


def load_all_vocabs_from_github():
    for file in os.listdir('.'):
        if file.startswith('gsq-') and file.endswith('.ttl'):
            g = rdflib.Graph().parse(file, format='turtle')
            print(file + " " + str(len(g)))

            q = '''
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?uri ?pl
                WHERE {
                    ?uri a owl:Ontology .
                    ?uri2 a skos:ConceptScheme ;
                        skos:prefLabel ?pl .
                }
            '''
            for r in g.query(q):
                base_url = r['uri']
                vocab_id = r['uri'].split('/')[-1]
                label = r['pl']

                load_one_vocab_from_github(vocab_id, base_url, label)


def list_repositories():
    r = requests.get(
        config.GRAPHDB_REPOS_URI,
        headers={'Accept': 'application/json'},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return json.loads(r.content.decode('utf-8'))


def make_config_file_contents(template_file, base_url, vocab_id, label):
    with open(template_file, 'r') as f:
        config_template_contents = f.read()
        return config_template_contents\
                    .replace('{repository_id}', vocab_id)\
                    .replace('{label}', label)\
                    .replace('{base_url}', base_url)


def create_repository(config_template_file_path, base_url, repo_id, repo_label):
    config_contents = make_config_file_contents(config_template_file_path,  base_url, repo_id, repo_label)

    r = requests.post(
        config.GRAPHDB_REPO_URI + '/' + repo_id,
        files={'config': ('config.ttl', config_contents)},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return r.status_code


def delete_repo(vocab_id):
    uri = config.GRAPHDB_REPO_URI + '/' + vocab_id
    r = requests.delete(
        uri,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
    )

    if r.status_code != 204:
        print(r.content.decode('utf-8'))
    return r.status_code


if __name__ == '__main__':
    # print(create_repository('repo-config.ttl.template', 'http://test.linked.data.gov.au/def/gsq-vocabs/', 'vocabs', 'GSQ Vocabularies'))
    # load_all_background_onts_from_github()
    load_all_vocabs_from_github()
