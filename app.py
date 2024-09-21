import requests
from flask import Flask, jsonify, request
import randoms
import logger
import json
from playfab import PlayFabAdminAPI, PlayFabSettings

app = Flask(__name__)
title = "96FD6"
secretkey = "U3BIUKPZXTKXXIINXFMQB4PJ1IUAMRDO3PYTA6T8WEGP5U6TZ8" #idk why it said secfret
coems = {} # bro why does this have ;


def authjh():
    return {"content-type": "application/json","X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "yesnt"

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
@app.route('/api/CachePlayFabId', methods=['POST'])
def cache_playfab_id():
    data = request.json
    send_to_discord_webhook(data)
    required_fields = ['Platform', 'SessionTicket', 'PlayFabId']
    if all([field in data for field in required_fields]):
        return jsonify({"Message": "PlayFabId Cached Successfully"}), 200
    else:
        missing_fields = [field for field in required_fields if field not in data]
        return jsonify({"Error": "Missing Data", "MissingFields": missing_fields}), 400

def send_to_discord_webhook(log_data):
    content = f"Auth Post Data: \n{json.dumps(log_data, indent=2)}\n"
    content += f"json\n{json.dumps(log_data, indent=2)}\n"
    requests.post(webhookUrl, json={"content": content})
    requests.post(webhookUrl, json={"content": content})

def send_to_discord_webhook2(nonce):
    content = f"Nonce Is: \n{json.dumps(nonce, indent=2)}\n"
    content += f"json\n{json.dumps(nonce, indent=2)}\n"
    requests.post(webhookUrl2, json={"content": content})
    requests.post(webhookUrl2, json={"content": content})
    

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

@app.route("/cbfn", methods=["POST","GET"])
def cfbn():
    name = request.args.get('name')
    BadNames = [
        "KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG",
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK",
        "DILDO", "HITLER", "KKX", "XKK", "NIGA", "NIGE", "NIG", "NI6", "PORN",
        "JEW", "JAXX", "TTTPIG", "SEX", "COCK", "CUM", "FUCK", "PENIS", "DICK",
        "ELLIOT", "JMAN", "K9", "NIGGA", "TTTPIG", "NICKER", "NICKA",
        "REEL", "NII", "@here", "!", " ", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9",
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "TTT"
    ];
    if name not in BadNames:result = 0
    else: result = 2
    return jsonify({"Message":"the name thingy worked!","Name":name,"Result":result})

@app.route("/gaa", methods=["POST", "GET"])
def gaa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson)

@app.route("/saa", methods=["POST", "GET"])
def saa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson) #qwizx did this on purpose bro i swear

@app.route("/grn", methods=["POST", "GET"])
def grn():
    return jsonify({"result": f"pluh!{randoms.randint(1000, 9999)}"})

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
if __name__ == "__main__":
  app.run(debug=True)