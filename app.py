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
        with open('/orxifytag/titleData.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading title data: {e}")
        return {}

def save_title_data_to_file(data):
    with open('orxifytag/titleData.json', 'w') as file:
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
def playfabauth():
    data = request.json
    print("Received data at /api/playfabauthenticate:", data)
    if 'CustomId' not in data:
        return jsonify({'Error': 'Bad Request', 'Message': 'CustomId is required'}), 400
    custom_id = data['CustomId']
    headers = {'Content-Type': 'application/json', 'X-SecretKey': SecretKey}

    # PlayFab login
    login_endpoint = f"https://{titleider}.playfabapi.com/Server/LoginWithServerCustomId"
    login_payload = {'TitleId': titleider, 'ServerCustomId': custom_id, 'CreateAccount': True}
    login_response = requests.post(login_endpoint, headers=headers, json=login_payload)
    if login_response.status_code == 200:
        write_playfab_id
        response_data = login_response.json()["data"]
        playfab_id = response_data['PlayFabId']
        session_ticket = response_data['SessionTicket']

        # For user authentication, use SessionTicket
        user_auth_headers = {'Content-Type': 'application/json', 'X-Authorization': session_ticket}
        link_endpoint = f"https://{titleider}.playfabapi.com/Client/LinkCustomID"
        link_payload = {'PlayFabId': playfab_id, 'CustomId': custom_id, 'ForceLink': True}
        link_response = requests.post(link_endpoint, headers=user_auth_headers, json=link_payload)
        if link_response.status_code == 200:
            print("CustomID successfully linked to the PlayFab account.")
        else:
            print(f"Failed to link CustomID: {link_response.status_code} - {link_response.text}")
        entityId = response_data['EntityToken']['Entity']['Id']
        entityType = response_data['EntityToken']['Entity']['Type']
        entityToken = response_data['EntityToken']['EntityToken']
        return jsonify({'SessionTicket': session_ticket, 'PlayFabId': playfab_id, 'EntityId': entityId, 'EntityType': entityType, 'EntityToken': entityToken}), 200

    elif login_response.status_code == 403:
        ban_info = login_response.json()
        if ban_info.get('errorCode') == 1002:
            ban_message = ban_info.get('errorMessage', "No ban message provided.")
            ban_details = ban_info.get('errorDetails', {})
            ban_expiration_key = next(iter(ban_details.keys()), None)
            ban_expiration_list = ban_details.get(ban_expiration_key, [])
            ban_expiration = ban_expiration_list[0] if len(ban_expiration_list) > 0 else "No expiration date provided."
            print(ban_info)
            return jsonify({'BanMessage': ban_message, 'BanExpirationTime': ban_expiration}), 403
        else:
            error_message = ban_info.get('errorMessage', 'Forbidden without ban information.')
            return jsonify({'Error': 'PlayFab Error', 'Message': error_message}), 403

    else:
        playfab_error = login_response.json().get("error", {})
        error_message = playfab_error.get("errorMessage", "Login failed")
        return jsonify({'Error': 'PlayFab Error', 'Message': error_message, 'PlayFabError': playfab_error}), login_response.status_code
@app.route('/')
def index():
    jsonify(return) "{
    "2024-05-AddOrRemoveDLCOwnershipV2": "false",
    "2024-05-BroadcastMyRoomV2": "false",
    "2024-05-ReturnCurrentVersionV2": " false",
    "2024-05-TryDistributeCurrencyV2": "false",
    "2024-06-CosmeticAuthenticationV2": "false",
    "2024-08-KIDIntegrationV1": "false",
    "AllowedClientVersions": "{\"clientVersions\":[\"beta1.1.1.86\",\"live1.1.1.86\",\"beta1.1.1.87\",\"live1.1.1.87\",\"beta1.1.1.51\",\"beta1.1.1.80\",\"beta1.1.1.88\",\"live1.1.1.88\"]}",
    "AutoMuteCheckedHours": "336",
    "AutoName_Adverbs": "[\"Cool\",\"Fine\",\"Bald\",\"Bold\",\"Half\",\"Only\",\"Calm\",\"Fab\",\"Ice\",\"Mad\",\"Rad\",\"Big\",\"New\",\"Old\",\"Shy\"]",
    "AutoName_Nouns": "[\"Gorilla\",\"Chicken\",\"Darling\",\"Sloth\",\"King\",\"Queen\",\"Royal\",\"Major\",\"Actor\",\"Agent\",\"Elder\",\"Honey\",\"Nurse\",\"Doctor\",\"Rebel\",\"Shape\",\"Ally\",\"Driver\",\"Deputy\"]",
    "BundleKioskButton": "\"DIS.GG/GORILLATAGV3\"",
    "BundleKioskSign": "\"DISCORD.GG/GORILLATAGV3\"",
    "BundleLargeSign": "\"DISCORD.GG/GORILLATAGV3\"",
    "CreditsData": "[{\"Title\":\"DEV TEAM\",\"Entries\":[\"Anton \\\"NtsFranz\\\" Franzluebbers\",\"Carlo Grossi Jr\",\"Cody O'Quinn\",\"Craig Abell\",\"David Neubelt\",\"David Yee\",\"Derek \\\"DunkTrain\\\" Arabian\",\"Duncan \\\"rev2600\\\" Carroll\",\"Elie Arabian\",\"Eric “8on2” Kearns\",\"John Sleeper\",\"Johnny Wing\",\"Jonathan \\\"Jonny D\\\" Dearborn\",\"Jonathan \\\"JHameltime\\\" Hamel\",\"Jordan \\\"CircuitLord\\\" J.\",\"Haunted Army\",\"Kaleb \\\"BiffBish\\\" Skillern\",\"Kerestell Smith\",\"Keith \\\"ElectronicWall\\\" Taylor\",\"Mark Putong\",\"Matt \\\"Crimity\\\" Ostgard\",\"Nick Taylor\",\"Riley O'Callaghan\",\"Ross Furmidge\",\"Zac Mroz\"]},{\"Title\":\"SPECIAL THANKS\",\"Entries\":[\"Alpha Squad\",\"Caroline Arabian\",\"Clarissa & Declan\",\"Calum Haigh\",\"EZ ICE\",\"Gwen\",\"Laura \\\"Poppy\\\" Lorian\",\"Lilly Tothill\",\"Meta\",\"Mighty PR\",\"Sasha \\\"Kayze\\\" Sanders\",\"Scout House\",\"The \\\"Sticks\\\"\"]},{\"Title\":\"MUSIC BY\",\"Entries\":[\"Stunshine\",\"David Anderson Kirk\",\"Jaguar Jen\",\"Audiopfeil\",\"Owlobe\"]}]",
    "DeployFeatureFlags": "{\"flags\":[{\"name\":\"2024-05-ReturnCurrentVersionV2\",\"value\":100,\"valueType\":\"percent\"},{\"name\":\"2024-05-ReturnMyOculusHashV2\",\"value\":100,\"valueType\":\"percent\"},{\"name\":\"2024-05-TryDistributeCurrencyV2\",\"value\":100,\"valueType\":\"percent\"},{\"name\":\"2024-05-AddOrRemoveDLCOwnershipV2\",\"value\":100,\"valueType\":\"percent\"},{\"name\":\"2024-05-BroadcastMyRoomV2\",\"value\":100,\"valueType\":\"percent\"},{\"name\":\"2024-06-CosmeticsAuthenticationV2\",\"value\":0,\"valueType\":\"percent\"},{\"name\":\"2024-08-KIDIntegrationV1\",\"value\":100,\"valueType\":\"percent\"}]}",
    "EnableCustomAuthentication": "false",
    "GorillanalyticsChance": "",
    "LatestPrivacyPolicyVersion": "1.1.28",
    "LatestTOSVersion": "11.05.22.2",
    "MOTD": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\n\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.29": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.34": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.41": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.45": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.46": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_1.1.52": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_CHRISTMAS2022": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_FALL_2022_ORXIFY": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_ORXIFY": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_SPRING_CLEANING": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_SPRING_COSMETICS": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_SUMMERCEL": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_SUMMERSPLASH_CUSTOMTAGGERS": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_WINTER_2023": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "MOTD_WINTER_FLASHBACK": "\u003Ccolor=red\u003EWELCOME TO\u003C/color\u003E \u003Ccolor=magenta\u003EORXIFY TAG (AKA ORXIFY TAG)\u003C/color\u003E\\n\u003Ccolor=red\u003EIT'S A GORILLA TAG CLONE THAT CAN DO\u003C/color\u003E \u003Ccolor=magenta\u003EANY\u003C/color\u003E \u003Ccolor=blue\u003EUPDATE POSSIBLE!\u003C/color\u003E\\n\u003Ccolor=purple\u003EOWNER:\u003C/color\u003E \u003Ccolor=red\u003EORXIFY\u003C/color\u003E\\n\\n\u003Ccolor=grey\u003EHELPERS: ORXIFY, S4GE\u003C/color\u003E\\n\u003Ccolor=cyan\u003EDISCORD.GG/ORXIFY TAG\u003C/color\u003E",
    "PrivacyPolicy_1.1.28": "\"DISCORD.GG/ORXIFY TAG\"",
    "PrivacyPolicy_2023.05.16": "\"DISCORD.GG/ORXIFY TAG\"",
    "PrivacyPolicy_2023.05.26": "\"DISCORD.GG/ORXIFY TAG\"",
    "PrivacyPolicy_2023.06.27": "\"DISCORD.GG/ORXIFY TAG\"",
    "PrivacyPolicy_2023.06.29": "\"DISCORD.GG/ORXIFY TAG\"",
    "PrivacyPolicy_2023.11.30": "\"DISCORD.GG/ORXIFY TAG\"",
    "SeasonalStoreBoardSign": "\"DISCORD.GG/ORXIFY TAG\"",
    "TOS_04.2.24.2": "\"JOIN DISCORD.GG/ORXIFY TAG\"",
    "TOS_11.05.22.2": "\"JOIN DISCORD.GG/ORXIFY TAG\"",
    "TOS_2023.05.16": "\"JOIN DISCORD.GG/ORXIFY TAG\"",
    "TOS_2023.05.26": "\"JOIN DISCORD.GG/ORXIFY TAG\"",
    "TOS_2023.11.30": "\"JOIN DISCORD.GG/ORXIFY TAG\"",
    "TOTD": "[{\"PedestalID\":\"CosmeticStand1\",\"ItemName\":\"LBAFF.\",\"StartTimeUTC\":\"2024-08-30T22:00:00.000Z\",\"EndTimeUTC\":\"2024-09-06T22:00:00.000Z\"},{\"PedestalID\":\"CosmeticStand2\",\"ItemName\":\"LBAFO.\",\"StartTimeUTC\":\"2024-08-30T22:00:00.000Z\",\"EndTimeUTC\":\"2024-09-06T22:00:00.000Z\"},{\"PedestalID\":\"CosmeticStand3\",\"ItemName\":\"LBAFR.\",\"StartTimeUTC\":\"2024-08-30T22:00:00.000Z\",\"EndTimeUTC\":\"2024-09-06T22:00:00.000Z\"}]",
    "Versions": "{\"CreditsData\":11,\"MOTD_1.1.38\":8,\"MOTD_1.1.39\":7,\"bundleData\":1,\"BundleLargeSign_1.1.40\":1,\"BundleBoardSign_1.1.40\":0,\"BundleKioskSign_1.1.40\":1,\"BundleKioskButton_1.1.40\":0,\"SeasonalStoreBoardSign_1.1.40\":0,\"MOTD_1.1.40\":0,\"MOTD_1.1.42\":2,\"MOTD_1.1.43\":0,\"SeasonalStoreBoardSign_1.1.43\":0,\"MOTD_1.1.45\":10,\"MOTD_1.1.46\":1}",
    "VotekickDuration": "10",
    "bannedusers_2024-09-10": "",
    "bannedusers_2024-09-11": "144",
    "bannedusers_2024-09-12": "143",
    "bannedusers_2024-09-13": "242",
    "bannedusers_2024-09-14": "328",
    "bannedusers_2024-09-15": "224",
    "bannedusers_2024-09-16": "174",
    "bannedusers_2024-09-17": "7",
    "bundleData": "{\"Items\":[{\"isActive\":false,\"skuName\":\"GLAMROCKERBUNDLE\",\"shinyRocks\":10000,\"playFabItemName\":\"GLAMROCKERBUNDLE\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":0,\"displayName\":\"GLAM ROCKER BUNDLE\"},{\"isActive\":false,\"skuName\":\"2024_cyber_monke_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABP.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":87,\"displayName\":\"Cyber Monke Pack\"},{\"isActive\":false,\"skuName\":\"2024_splash_dash_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABO.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":85,\"displayName\":\"Splash and Dash Pack\"},{\"isActive\":false,\"skuName\":\"2024_shiny_rock_special\",\"shinyRocks\":2200,\"playFabItemName\":\"LSABN.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":83,\"displayName\":\"Shiny Rock Special\"},{\"isActive\":false,\"skuName\":\"2024_climb_stoppers_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABM.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":82},{\"isActive\":true,\"skuName\":\"2024_glam_rocker_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABL.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":80},{\"isActive\":false,\"skuName\":\"2024_monke_monk_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABK.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":78},{\"isActive\":false,\"skuName\":\"2024_leaf_ninja_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABJ.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":76},{\"isActive\":false,\"skuName\":\"2024_gt_monke_plush\",\"shinyRocks\":0,\"playFabItemName\":\"LSABI.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":73},{\"isActive\":false,\"skuName\":\"2024_beekeeper_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABH.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":73},{\"isActive\":false,\"skuName\":\"2024_i_lava_you_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABG.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":71},{\"isActive\":false,\"skuName\":\"2024_mad_scientist_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABF.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":69},{\"isActive\":false,\"skuName\":\"2023_holiday_fir_pack\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABE.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":63},{\"isActive\":false,\"skuName\":\"2023_spider_monke_bundle\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABD.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":59},{\"isActive\":false,\"skuName\":\"2023_caves_bundle\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABC.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":54},{\"isActive\":false,\"skuName\":\"2023_summer_splash_bundle\",\"shinyRocks\":10000,\"playFabItemName\":\"LSABA.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":46},{\"isActive\":false,\"skuName\":\"2023_march_pot_o_gold\",\"shinyRocks\":5000,\"playFabItemName\":\"LSAAU.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":39},{\"skuName\":\"2023_sweet_heart_bundle\",\"playFabItemName\":\"LSAAS.\",\"shinyRocks\":0,\"isActive\":false},{\"skuName\":\"2022_launch_bundle\",\"playFabItemName\":\"LSAAP2.\",\"shinyRocks\":10000,\"isActive\":false},{\"skuName\":\"early_access_supporter_pack\",\"playFabItemName\":\"Early Access Supporter Pack\",\"shinyRocks\":0,\"isActive\":false}]}"
  }"

@app.route('/api/CachePlayFabId', methods=['POST'])
def cache_playfab_id():
    data = request.json
