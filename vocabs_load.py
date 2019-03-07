import requests
import json
import os
import rdflib

import _config as config


# create-repos or load-data
def map_from_vocab_files(func):
    if func == 'create-repos':
        print('Creating Repos')
        print()
    elif func == 'load-data':
        print('Loading Data')
        print()

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

                if func == 'create-repos':
                    print()
                    print('Creating ' + label)
                    create_repository('repo-config.ttl.template', base_url, vocab_id, label)
                elif func == 'load-data':
                    print()
                    print('Loading ' + label)
                    load_vocab_data_from_github(base_url, vocab_id, label)


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


def create_repository(config_template_file_path, base_url, vocab_id, label):
    config_contents = make_config_file_contents(config_template_file_path,  base_url, vocab_id, label)

    r = requests.post(
        config.GRAPHDB_REPOS_URI,
        files={'config': ('config.ttl', config_contents)},
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD)
    )

    return r.status_code


def load_vocab_data_from_github(vocab_id, base_url, label):
    named_graph = base_url.rstrip('/')
    uri = config.GRAPHDB_LOAD_DATA_URI.replace('{repository}', vocab_id)
    r = requests.post(
        uri,
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': base_url,
            'context': named_graph,
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
                named_graph  # same as Context
            ],
            'status': 'PENDING',
            'timestamp': 0,
            'type': 'string',
            'xRequestIdHeaders': 'string'
        }
    )

    if r.status_code == 400:
        print(r.content.decode('utf-8'))
    return r.status_code


if __name__ == '__main__':
    map_from_vocab_files('create-repos')
    map_from_vocab_files('load-data')

