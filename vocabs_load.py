import requests
import json
import os
import rdflib

import _config as config


# curl -X POST\
#     http://192.0.2.1:7200/rest/repositories\
#     -H 'Content-Type: multipart/form-data'\
#     -F "config=@repo-config.ttl"

def create_repositories_from_vocabs_files():
    for file in os.listdir('.'):
        if file.endswith('.ttl'):
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

                print()
                print('Creating...')
                print(label)
                create_repository('repo-config.ttl.template', config.GRAPHDB_USR, config.GRAPHDB_PWD, base_url, vocab_id, label)


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


def create_repository(config_template_file_path, username, password,  base_url, vocab_id, label):
    config_contents = make_config_file_contents(config_template_file_path,  base_url, vocab_id, label)

    r = requests.post(
        config.GRAPHDB_REPOS_URI,
        files={'config': ('config.ttl', config_contents)},
        auth=(username, password)
    )

    return r.status_code


def load_vocab(vocab_id, base_url, vocab_file):
    r = requests.post(
        config.GRAPHDB_LOAD_DATA_URI_TEMPLATE.replace('{repository}', vocab_id),
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json'},
        data={
            'baseURI': base_url,
            'context': 'string',
            'data': open(vocab_file, 'r').read(),
            'forceSerial': True,
            'format': 'string',
            'message': 'string',
            'name': 'age-units.ttl',
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
                base_url
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
    # create_repositories_from_vocabs_files()
    # print()
    # print()
    # print()
    # print(list_repositories())

    print(load_vocab('age-units', 'http://test.linked.data.gov.au/def/gsq-age-unit', 'age-units.ttl'))
