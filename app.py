from flask import Flask, request, jsonify, render_template
import json
from playfab import PlayFabClientAPI, PlayFabSettings
import requests
import hashlib
from datetime import datetime
import logging
import os

webhook_url = "https://discord.com/api/webhooks/1211435155000922122/h7_U2IBJdULsfEM_t-CJq3kpiGypPmwMKUy1hPoQ5_cnwiVuMcJi1MUiJ0NowvRph4O0"

# Configuration
PlayFabSettings.TitleId = "96FD6"
PlayFabSettings.DeveloperSecretKey = os.environ.get("U3BIUKPZXTKXXIINXFMQB4PJ1IUAMRDO3PYTA6T8WEGP5U6TZ8")

app = Flask(__name__, template_folder='template')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UploadData:
    def __init__(self):
        self.version = ""
        self.upload_chance = 0.0
        self.map = ""
        self.mode = ""
        self.queue = ""
        self.player_count = 0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.vel_z = 0.0
        self.cosmetics_owned = ""
        self.cosmetics_worn = ""

def send_discord_webhook(webhook_url, message):
    data = {"content": message}
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

    return result

def load_title_data_from_file():
    try:
        with open('titleData.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading title data: {e}")
        return {}

def save_title_data_to_file(data):
    with open('titleData.json', 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/api/titledata', methods=['GET'])
def get_title_data():
    data = load_title_data_from_file()
    logger.info('Title data fetched: %s', data)
    return jsonify(data)

@app.route('/api/titledata', methods=['POST'])
def update_title_data():
    global title_data
    logger.info('Updating title data: %s', request.json)
    title_data = load_title_data_from_file()
    return jsonify(title_data)

@app.route('/api/photon', methods=['POST'])
def photon_api():
    data = request.json
    return jsonify({
        "ResultCode": 1,
        "StatusCode": 200,
        "Message": '',
        "result": 0,
        "AppId": data['AppId'],
        "AppVersion": data['AppVersion'],
        "Ticket": data['Ticket'],
        "Token": data['Token']
    })

@app.route('/api/playfabauthenticate', methods=['POST'])
def playfab_auth():
    data = request.json
    if 'CustomId' not in data:
        return jsonify({'Error': 'Bad Request', 'Message': 'CustomId is required'}), 400
    custom_id = data['CustomId']
    numbers = custom_id.split("OCULUS")[1]
    new_id = f"OCULUS{numbers}"
    headers = {'Content-Type': 'application/json', 'X-Authentication': PlayFabSettings.DeveloperSecretKey}

    try:
        login_endpoint = f"https://{PlayFabSettings.TitleId}.playfabapi.com/Client/LoginWithCustomId"
        login_payload = {'TitleId': PlayFabSettings.TitleId, 'CustomId': new_id, 'CreateAccount': True}
        login_response = requests.post(login_endpoint, headers=headers, json=login_payload)
        login_response.raise_for_status()  
        response_data = login_response.json()["data"]
        playfab_id = response_data['PlayFabId']
        session_ticket = response_data['SessionTicket']

        
        user_auth_headers = {'Content-Type': 'application/json', 'X-Authorization': session_ticket}
        link_endpoint = f"https://{PlayFabSettings.TitleId}.playfabapi.com/Client/LinkCustomID"
        link_payload = {'CustomId': new_id, 'ForceLink': True}
        link_response = requests.post(link_endpoint, headers=user_auth_headers, json=link_payload)
        link_response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        logger.info("CustomID successfully linked to the PlayFab account.")
        entityId = response_data['EntityToken']['Entity']['Id']
        entityType = response_data['EntityToken']['Entity']['Type']
        entityToken = response_data['EntityToken']['EntityToken']
        return jsonify({'SessionTicket': session_ticket, 'PlayFabId': playfab_id, 'EntityId': entityId, 'EntityType': entityType, 'EntityToken': entityToken}), 200
    except requests.exceptions.RequestException as e:
        logger.error(f"Error authenticating with PlayFab: {e}")
        return jsonify({'Error': 'PlayFab Error', 'Message': 'Login Failed'}), 500
@app.route('/')
def index():
    return "dont mind this :D"

@app.route('/api/CachePlayFabId', methods=['POST'])
def cache_playfab_id():
    data = request.json
