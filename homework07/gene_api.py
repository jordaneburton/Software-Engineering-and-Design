import redis
from flask import Flask, request
import requests
import json
import yaml

app = Flask(__name__)

def get_redis_client():
    return redis.Redis(host='redis-db', port=6379, db=0)

rd = get_redis_client()

@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def data():
    """
    Performs one of three tasks:

    - Put data into Redis database
    - Returns all data from Redis database
    - Deletes data from Redis database
    """

    if request.method == 'POST':
        data_url = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json'
        response = requests.get(url)
        if response.status_code != 200:
            return 'Error: Failed to retrieve data'
        else:
            data = json.loads(response.text)
            rd.set('gene_data', json.dumps(data))
            return 'Posted gene data'

    elif request.method == 'GET':
        try:
            return json.loads(rd.get('gene_data').decode('utf-8'))
        except KeyError:
            return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data"
        
    elif request.method == 'DELETE':
        rd.delete('gene_data')
        return 'Deleted gene data'

@app.route('/genes', methods=['GET'])
def get_genes() -> list:
    """
    Returns json-formatted list of all hgnc_ids
    """
    list_of_hgnc_ids = []
    try:
        json_data = json.loads(rd.get('gene_data').decode('utf-8'))

        for i in range(len(json_data['response'])):
            list_of_hgnc_ids.append(json_data['response']['docs'][i]['hgnc_id']
        return list_of_hgnc_ids
    except Exception as err:
        return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data"

@app.route('/genes/<string: hgnc_id>', methods=['GET'])
def get_genes_hgnc(hgnc_id: str) -> dict:
    """
    Args: hgnc_id - identifies which gene to pull data from

    Returns all data associated with <hgnc_id>
    """
    try:
        json_data = json.loads(rd.get('gene_data').decode('utf-8'))
        for hgnc in json_data['response']['docs']:
            if hgnc['hgnc_id'] == hgnc_id:
                return [hgnc]
    except TypeError:
        return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data"
    except ValueError as err:
        return "Invalid Input for: 'hgnc_id'"

def get_config():
    default_config = {"debug": True}
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Couldn't load the config file; details: {e}")
        return default_config

if __name__ == '__main__':
    config = get_config()
    if config.get('debug', True):
        app,run(debug=True, host='0.0.0.0')
    else:
        app.run(debug=True, host='0.0.0.0')
