import redis
from flask import Flask, request, send_file
import requests
import json
import yaml
import os
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def get_redis_client():
    redis_ip = os.environ.get('REDIS_HOST')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=0)

rd = get_redis_client()
rd_img = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=1)

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
        response = requests.get(data_url)
        if response.status_code == 200:
            global gene_data
            gene_data = json.loads(response.text)
            rd.set('gene_data', json.dumps(gene_data))
            return 'Posted gene data\n'
        else:
            return 'Error: Failed to retrieve data\n'

    elif request.method == 'GET':
        try:
            data = rd.get('gene_data')
            return json.loads(data)
        except:
            return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data\n"
        
    elif request.method == 'DELETE':
        rd.delete('gene_data')
        return 'Deleted gene data\n'

@app.route('/genes', methods=['GET'])
def get_genes() -> list:
    """
    Returns json-formatted list of all hgnc_ids
    """
    list_of_hgnc_ids = []
    try:
        data = rd.get('gene_data')
        gene_data = json.loads(data)

        for i in range(len(gene_data['response']['docs'])):
            list_of_hgnc_ids.append(gene_data['response']['docs'][i]['hgnc_id'])
        return list_of_hgnc_ids
    except:
        return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data\n"

@app.route('/genes/<string:hgnc_id>', methods=['GET'])
def get_genes_hgnc(hgnc_id: str) -> dict:
    """
    Args: hgnc_id - identifies which gene to pull data from

    Returns all data associated with <hgnc_id>
    """
    try:
        gene_data = data()
        for hgnc in gene_data['response']['docs']:
            if hgnc['hgnc_id'] == hgnc_id:
                return [hgnc]
    except TypeError:
        return "No data found. Use 'curl -X POST localhost:5000/data' to fetch data\n"
    except ValueError as err:
        return "Invalid Input for: 'hgnc_id'\n"

@app.route('/image', methods=['POST', 'GET', 'DELETE'])
def get_image():
    """
    Returns a plot of data in a second flask tab. The plot can be posted, 
    pulled up, or deleted
    """
    
    if request.method == 'POST':
        try:
            """
            Use data to fill two lists: one with locus group names and one with
            number of genes in each group. Plotting two ordered lists seemed
            easier than trying to plot a dict object.
            """
            data = rd.get('gene_data')
            gene_data = json.loads(data)

            locus_list = []
            locus_count = []
             
            for i in gene_data['response']['docs']:
                locus_included = False
                for j in locus_list:
                    if i['locus_group'] == [j]: 
                        locus_included = True
                        index = int(locus_list.index(i['locus_group']))
                        locus_count[index] = 1 + locus_count[index] 
                        break
                if not locus_included:
                    locus_list.append(i['locus_group'])       
                    locus_count.append(1)
            
            poserror = str(len(locus_list)) + " " + str(len(locus_count)) + "\n"
            if not (len(locus_list) == len(locus_count)): raise AssertionError(poserror)
            
            x = list(range(1,len(locus_count)))
            plt.figure(figsize=(15,15))
            plt.hist(locus_count)
            plt.xlabel(locus_list)
            plt.ylabel('Number of Genes')
            plt.title('How Many Genes Are In Each Locus Group')
            plt.savefig('graph.png')
            file_bytes = open('./graph.png', 'rb').read()
            rd_img.set('key', file_bytes)
            
            return "Image posted\n"

        except AssertionError as e:
            return "Count and List are not same length\n" + e.args

        except SyntaxError:
            return "Error: Check to see if data is posted\n"

    elif request.method == 'GET':
        try:
            path = './graph.png'
            with open(path, 'wb') as f:
                f.write(rd_img.get('key'))
            return send_file(path, mimetype='graph/png', as_attachment=True)
        except TypeError:
            return "Error: Both the data and the image must be posted\n"

    elif request.method == 'DELETE':
        rd_img.delete('key')
        return "Image deleted\n"

def get_config() -> dict:
    default_config = {"debug": True}
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Couldn't load the config file; details: {e}\n")
        return default_config

if __name__ == '__main__':
    config = get_config()
    if config.get('debug', True):
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(debug=True, host='0.0.0.0')
