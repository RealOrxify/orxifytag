from flask import Flask, request, jsonify, render_template
import json
from playfab import PlayFabClientAPI, PlayFabSettings
import requests
import hashlib
from datetime import datetime
import logging
import os
import base64



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
def get_file_contents(data):
    # Decode the base64-encoded content
    content_bytes = base64.b64decode(data["content"])
    content_str = content_bytes.decode('utf-8')

    # Parse the JSON content
    content_json = json.loads(content_str)

    # Return the JSON content as a JSON response
    return jsonify(content_json)

data = {
  "name": "titleData.json",
  "path": "titleData.json",
  "sha": "27e5ddc407e4ddc80f84c221c5ee7b04586feea4",
  "size": 17069,
  "url": "https://api.github.com/repos/RealOrxify/orxifytag/contents/titleData.json?ref=main",
  "html_url": "https://github.com/RealOrxify/orxifytag/blob/main/titleData.json",
  "git_url": "https://api.github.com/repos/RealOrxify/orxifytag/git/blobs/27e5ddc407e4ddc80f84c221c5ee7b04586feea4",
  "download_url": "https://raw.githubusercontent.com/RealOrxify/orxifytag/main/titleData.json",
  "type": "file",
  "content": "ew0KICAiMjAyNC0wNS1BZGRPclJlbW92ZURMQ093bmVyc2hpcFYyIjogImZh\nbHNlIiwNCiAgIjIwMjQtMDUtQnJvYWRjYXN0TXlSb29tVjIiOiAiZmFsc2Ui\nLA0KICAiMjAyNC0wNS1SZXR1cm5DdXJyZW50VmVyc2lvblYyIjogIiBmYWxz\nZSIsDQogICIyMDI0LTA1LVRyeURpc3RyaWJ1dGVDdXJyZW5jeVYyIjogImZh\nbHNlIiwNCiAgIjIwMjQtMDYtQ29zbWV0aWNBdXRoZW50aWNhdGlvblYyIjog\nImZhbHNlIiwNCiAgIjIwMjQtMDgtS0lESW50ZWdyYXRpb25WMSI6ICJmYWxz\nZSIsDQogICJBbGxvd2VkQ2xpZW50VmVyc2lvbnMiOiAie1wiY2xpZW50VmVy\nc2lvbnNcIjpbXCJiZXRhMS4xLjEuODZcIixcImxpdmUxLjEuMS44NlwiLFwi\nYmV0YTEuMS4xLjg3XCIsXCJsaXZlMS4xLjEuODdcIixcImJldGExLjEuMS41\nMVwiLFwiYmV0YTEuMS4xLjgwXCIsXCJiZXRhMS4xLjEuODhcIixcImxpdmUx\nLjEuMS44OFwiXX0iLA0KICAiQXV0b011dGVDaGVja2VkSG91cnMiOiAiMzM2\nIiwNCiAgIkF1dG9OYW1lX0FkdmVyYnMiOiAiW1wiQ29vbFwiLFwiRmluZVwi\nLFwiQmFsZFwiLFwiQm9sZFwiLFwiSGFsZlwiLFwiT25seVwiLFwiQ2FsbVwi\nLFwiRmFiXCIsXCJJY2VcIixcIk1hZFwiLFwiUmFkXCIsXCJCaWdcIixcIk5l\nd1wiLFwiT2xkXCIsXCJTaHlcIl0iLA0KICAiQXV0b05hbWVfTm91bnMiOiAi\nW1wiR29yaWxsYVwiLFwiQ2hpY2tlblwiLFwiRGFybGluZ1wiLFwiU2xvdGhc\nIixcIktpbmdcIixcIlF1ZWVuXCIsXCJSb3lhbFwiLFwiTWFqb3JcIixcIkFj\ndG9yXCIsXCJBZ2VudFwiLFwiRWxkZXJcIixcIkhvbmV5XCIsXCJOdXJzZVwi\nLFwiRG9jdG9yXCIsXCJSZWJlbFwiLFwiU2hhcGVcIixcIkFsbHlcIixcIkRy\naXZlclwiLFwiRGVwdXR5XCJdIiwNCiAgIkJ1bmRsZUtpb3NrQnV0dG9uIjog\nIlwiRElTLkdHL0dPUklMTEFUQUdWM1wiIiwNCiAgIkJ1bmRsZUtpb3NrU2ln\nbiI6ICJcIkRJU0NPUkQuR0cvR09SSUxMQVRBR1YzXCIiLA0KICAiQnVuZGxl\nTGFyZ2VTaWduIjogIlwiRElTQ09SRC5HRy9HT1JJTExBVEFHVjNcIiIsDQog\nICJDcmVkaXRzRGF0YSI6ICJbe1wiVGl0bGVcIjpcIkRFViBURUFNXCIsXCJF\nbnRyaWVzXCI6W1wiQ

webhook_url = "https://discord.com/api/webhooks/1211435155000922122/h7_U2IBJdULsfEM_t-CJq3kpiGypPmwMKUy1hPoQ5_cnwiVuMcJi1MUiJ0NowvRph4O0"
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
    data = get_file_contents(data)  # Call the get_file_contents function
    logger.info('Title data fetched: %s', data)
    return jsonify(data)  # Return the decoded JSON content

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
