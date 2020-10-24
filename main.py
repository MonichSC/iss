from flask import Flask, render_template, request, jsonify
from google.oauth2 import service_account
import base64, time, json
from googleapiclient import discovery
from google.cloud import pubsub_v1
from google.cloud import storage

SERVICE_ACCOUNT_FILE = 'stacja-pogodowa-auet-2019-a938041eb774.json'
scopes = ['https://www.googleapis.com/auth/bigquery']
project_id = "stacja-pogodowa-auet-2019"
registry_id = "rejestrStacjaPogodowa"
device_id = "stacjaPogodowa1"
cloud_region = "europe-west1"

#######################################################################
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE)


#*********************************************************************
def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)


client_IoT = get_client(SERVICE_ACCOUNT_FILE)
device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
    project_id, cloud_region, registry_id, device_id)


def send_commends(command):
    config_body = {
        'binaryData':
        base64.urlsafe_b64encode(command.encode('utf-8')).decode('ascii')
    }
    return client_IoT.projects().locations().registries().devices().sendCommandToDevice\
        (name=device_path, body=config_body).execute()


def send_conf(conf):
    config_body = {
        'binaryData':
        base64.urlsafe_b64encode(conf.encode('utf-8')).decode('ascii')
    }
    return client_IoT.projects().locations().registries().devices().modifyCloudToDeviceConfig\
        (name=device_path, body=config_body).execute()


#**********************************************************************

client_storage = storage.Client(credentials=credentials, project=project_id)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)


def callback(message):

    actual_message = (message.data)
    message.ack()
    actual_message = actual_message.decode('utf8').replace("'", "")
    actual_message = json.loads(actual_message)

    if (message.attributes['subFolder'] == "actual"):
        s = json.dumps(actual_message, indent=4)
        actual = open("actual.json", "w+")
        actual.write(s)
        actual.close()
        print("odebrałem dane actual")
    else:
        trend = open("trends.json", "r")
        trends_data = trend.read()
        trend.close()
        trends_data = json.loads(trends_data)
        if (len(trends_data) >= 432):
            trends_data.remove(trends_data[0])
        trends_data.append(actual_message)
        s = json.dumps(trends_data, indent=4)
        trend = open("trends.json", "w+")
        trend.write(s)
        trend.close()
        print("odebrałem dane trends")


#subscriber.subscribe(subscriber.subscription_path("stacja-pogodowa-auet-2019", "actual"), callback=callback)
#subscriber.subscribe(subscriber.subscription_path("stacja-pogodowa-auet-2019", "trends"), callback=callback)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/trends')
def trends():
    return render_template("trends.html")


@app.route('/confi')
def confi():
    return render_template("confi.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/actual', methods=['GET', 'POST'])
def actual():
    if request.method == 'POST':
        bucket = client_storage.get_bucket('testowy_zasobnik')
        blob = bucket.get_blob('temp_files_folder/actual.json')
        blob.download_to_filename("actual.json")
        actual = open("actual.json", "r")
        actual_data = actual.read()
        actual.close()
        actual_data = json.loads(actual_data)
        print("odczytuje plik")
        print(actual_data)
        return jsonify(actual_data)


@app.route('/trends_res', methods=['GET', 'POST'])
def trends_res():
    tab = ["temp", "insol", "pres", "W_speed", "W_dir"]
    if request.method == 'POST':

        lista = []
        bucket = client_storage.get_bucket('testowy_zasobnik')
        blob = bucket.get_blob('temp_files_folder/trends.json')
        blob.download_to_filename("trends.json")
        trends = open("trends.json", "r")
        data = trends.read()
        trends.close()
        data = json.loads(data)
        print(request.form['get_data'])
        print(data)
        if request.form['prezentacja'] == 'tabela':
            return jsonify(data)

        else:
            for row in data:
                DANE = {
                    'time': row['time'],
                    'war':
                    row[('{}').format(tab[int(request.form['get_data'])])]
                }
                print(DANE)
                lista.append(DANE)
            return jsonify(lista)


@app.route('/confi_ajax', methods=['GET', 'POST'])
def confi_ajax():
    if request.method == 'POST':
        if request.form['what_to_do'] == "send_comand_on":
            send_commends('dioda_on')
            return jsonify({'status': "wysłano komende D_ON"})
        elif request.form['what_to_do'] == "send_comand_off":
            send_commends('dioda_off')
            return jsonify({'status': "wysłano komende D_OFF"})
        elif request.form['what_to_do'] == "update_konfi":
            konfiguracja="Okres archiwizacji:" + request.form['confi_time']
            send_conf(konfiguracja)
            return jsonify({'status': "zaktualizowano"})
        elif request.form['what_to_do'] == "clear_file":
            bucket = client_storage.get_bucket('testowy_zasobnik')
            blob = bucket.get_blob('temp_files_folder/trends.json')
            blob.upload_from_string('[]')
            return jsonify({'status': "wyczyszczono plik"})


@app.route('/tech_data', methods=['GET', 'POST'])
def tech_data():
    if request.method == 'POST':
      bucket = client_storage.get_bucket('testowy_zasobnik')
      blob = bucket.get_blob('temp_files_folder/actual.json')
      blob.download_to_filename("actual.json")
      actual = open("actual.json", "r")
      actual_data = actual.read()
      actual.close()
      actual_data = json.loads(actual_data)
      print("odczytuje plik")
      print(actual_data)
      return jsonify(actual_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
