import json
from elasticsearch import Elasticsearch, helpers
import os

def connect_elasticsearch():
    try:
        es = Elasticsearch(
            [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
        
            verify_certs=False,  # Disable SSL certificate verification
            ssl_show_warn=False  # Optionally suppress warnings about this
        )
        if es.ping():
            print('Elasticsearch connected')
        else:
            print('Could not connect to Elasticsearch')
        return es
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None

def create_index(es, index_name):
    # Define index settings and mappings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "authors": {"type": "text"},
                "abstract": {"type": "text"},
                "keywords": {"type": "text"},
                "Keywordfs": {"type": "text"},
                "volume_title": {"type": "text"},
                "conference_name": {"type": "text"}
            }
        }
    }
    es.indices.create(index=index_name, ignore=400, body=settings)

def load_json_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def index_data(es, index_name, data):
    if isinstance(data, list):
        actions = [
            {
                "_index": index_name,
                "_source": item
            }
            for item in data
        ]
        helpers.bulk(es, actions)
    else:
        es.index(index=index_name, body=data)

def index_all_json_files(es, index_name, json_dir):
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            file_path = os.path.join(json_dir, json_file)
            data = load_json_data(file_path)
            index_data(es, index_name, data)
            print(f"Indexed {json_file} to Elasticsearch")