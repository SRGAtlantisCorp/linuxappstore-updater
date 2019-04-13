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
    feedJson = getFeed("https://flathub.org/api/v1/apps/")
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
    payload = {}
    payload["ApiKey"] = apiKey
    Apps = []

    for item in feedJson:
        name = item["name"]
        if not name:
            continue
        icon = item["iconDesktopUrl"]
        if not str(icon).startswith("https"):
            icon = "https://flathub.org" + icon
        identifier = item["flatpakAppId"]
        if not identifier:
            print("App={} missing identifier".format(name))
            continue
        src = "https://flathub.org/apps/details/" + identifier
        date_added = item["inStoreSinceDate"]
        created_at_datetime = dateutil.parser.parse(date_added)
        created_at = created_at_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        last_updated_datetime = datetime.datetime.now()
        last_updated = item["currentReleaseDate"]
        if last_updated:
            last_updated_datetime = dateutil.parser.parse(last_updated)
        last_updated = last_updated_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        current_version = item["currentReleaseVersion"]
        print("name: {}".format(name))
        print("\ttype: 2")
        print("\ticon: {}".format(icon))
        print("\tdownload: {}".format(src))
        print("\tcreated_at: {}".format(created_at))
        print("\tlast_updated: {}".format(last_updated))
        print("\tcurrent_version: {}".format(current_version))
        
        app = {"id": 0, "name":name, "type":2, "dateAdded":created_at, "lastUpdated":last_updated,
        "src":src, "icon":icon, "currentVersion":current_version, "identifier":identifier}
        Apps.append(app)
    payload["Apps"] = Apps
    postData(postUrl, payload)            

scrap()