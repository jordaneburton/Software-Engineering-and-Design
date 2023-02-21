from flask import Flask
import requests
import xmltodict
import math

app = Flask(__name__)
iss_url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
response = requests.get(iss_url)
iss_response = xmltodict.parse(response.text)
iss_data = iss_response['ndm']['oem']['body']['segment']['data']

@app.route('/', methods=['GET'])
def get_data():
    result = []
    stateVectors = []
    for i in iss_data['stateVector']:
        stateVectors.append(i['EPOCH'])
        stateVectors.append('X = ' + i['X']['#text'] + i['X']['@units'])
        stateVectors.append('Y = ' + i['Y']['#text'] + i['Y']['@units'])
        stateVectors.append('Z = ' + i['Z']['#text'] + i['Z']['@units'])
        
        stateVectors.append('X_DOT = ' + i['X_DOT']['#text'] + i['X_DOT']['@units'])
        stateVectors.append('Y_DOT = ' + i['Y_DOT']['#text'] + i['Y_DOT']['@units'])
        stateVectors.append('Z_DOT = ' + i['Z_DOT']['#text'] + i['Z_DOT']['@units'])
        
        result.append(stateVectors)
        stateVectors = []
    return result

@app.route('/epoch', methods=['GET'])
def epoch():
    list_epochs = []
    epoch_i = ''
    for i in iss_data['stateVector']:
        epoch_i = i['EPOCH']
        list_epochs.append(epoch_i)
    
    result = ('List of all available EPOCHs: \n {}\n'.format(list_epochs))
    return result

@app.route('/epoch/<int:epoch>', methods=['GET'])
def get_epoch(epoch):
    result = ('EPOCH entry {}: {}\n'
            .format(epoch, iss_data['stateVector'][epoch]['EPOCH']))
    return result

@app.route('/epoch/<int:epoch>/speed', methods=['GET'])
def get_speed(epoch):
    x_dot = float(iss_data['stateVector'][epoch]['X_DOT']['#text'])
    y_dot = float(iss_data['stateVector'][epoch]['Y_DOT']['#text'])
    z_dot = float(iss_data['stateVector'][epoch]['Z_DOT']['#text'])
    units = str(iss_data['stateVector'][epoch]['Z_DOT']['@units'])

    speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
    result = ('EPOCH: {}\nCalculated speed to be: {} {}\n'
            .format(iss_data['stateVector'][epoch]['EPOCH'],speed, units))
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

