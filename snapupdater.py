import json
import requests
import datetime
import dateutil.parser

def getSettings(file_name):    
    try:
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
                return data
        except:
            raise ValueError("Could not open file={}".format(file_name))     
    except ValueError as e:
        print(e)

def getFeed(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        print("Failed to retrieve feed.")

def postData(url, content):
    print("Posting data to url={}".format(url))
    requests.post(url, json=content)

def scrap():
    feedJson = getFeed("https://search.apps.ubuntu.com/api/v1/search")
    if feedJson is None:
        return

    settings = getSettings("settings.json")
    if settings is None:
        return
    
    apiKey = settings["ApiKey"]
    if not apiKey:
        print("ApiKey does not exist.")
        return

    postUrl = settings["PostUrl"]
    if not postUrl:
        print("PostUrl does not exist.")
        return

    embedded = feedJson["_embedded"]

    if not embedded:
        print("_embedded does not exist.")
        return

    snaps = embedded["clickindex:package"]

    if not snaps:
        print("clickindex:package does not exist.")
        return

    payload = {}
    payload["ApiKey"] = apiKey
    Apps = []

    for snap in snaps:
        title = snap["title"]
        current_version = snap["version"]
        icon = snap["icon_url"]
        src = snap["download_url"]
        identifier = snap["snap_id"]
        date_published = snap["date_published"]
        date_added_datetime = dateutil.parser.parse(date_published)
        date_added_formatted = date_added_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        last_updated = snap["last_updated"]
        last_updated_datetime = dateutil.parser.parse(last_updated)
        last_updated_formatted = last_updated_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        print("name: {} identifier={}".format(title, identifier))
        print("\ttype: 3")
        print("\ticon: {}".format(icon))
        print("\tdownload: {}".format(src))
        print("\tcurrent_version: {}".format(current_version))
        print("\tdate_added: {}".format(date_added_formatted))
        print("\tlast_updated: {}".format(last_updated_formatted))
        print()
        app = {"id": 0, "name":title, "type":3, "dateAdded":date_added_formatted, "lastUpdated":last_updated_formatted,
        "src":src, "icon":icon, "currentVersion":current_version, "identifier":identifier}
        Apps.append(app)
    payload["Apps"] = Apps
    postData(postUrl, payload) 
scrap()