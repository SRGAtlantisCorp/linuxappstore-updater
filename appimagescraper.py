import json
import requests
import datetime
import dateutil.parser
import collections

def getSettings(file_name):
    settings = {}
    try:
        with open(file_name) as json_file:  
            data = json.load(json_file)
            apiKey = data["ApiKey"]
            if not apiKey:
                raise Exception() 
            postUrl = data["PostUrl"]
            if not postUrl:
                raise Exception()
            settings["ApiKey"] = apiKey            
            settings["PostUrl"] = postUrl               
    except:
        print("Could not open ApiKey from file={}".format(file_name))
    return settings


def getIconAsString(icons):
    if icons and len(icons) > 0:
        return icons[0]
    else:
        return None

def getDownloadLink(data):
    if (data):
        for item in data:
            type = item["type"]
            if type == "Download":
                download_link = item["url"]
                return download_link
    else:
        return None

def getGithubReleaseApiLink(link):
    if link:
        return str(link).replace("github.com/", "api.github.com/repos/")
    else:
        return None

def getExtraDetailsFromGithubApi(api_url):
    if api_url:
        r = requests.get(api_url)
        j = r.json()
        for item in j:
            prerelease = item["prerelease"]
            if not prerelease:
                tag_name = item["tag_name"]
                created_at = item["created_at"]
                if created_at:                    
                    created_at_time = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ") 
                    created_at = created_at_time.strftime("%Y-%m-%dT%H:%M:%S")                   
                published_at = item["published_at"]
                if published_at:
                    published_at_time = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    published_at = published_at_time.strftime("%Y-%m-%dT%H:%M:%S")                
                return {'created_at':created_at, 'published_at':published_at, 'tag_name':tag_name }

def postData(url, content):
    print("Posting data to url={}".format(url))
    requests.post(url, json=content)

def scrap():
    r = requests.get('https://appimage.github.io/feed.json')
    j = r.json()
    items = j["items"]
    count = 0
    payload = {}
    settings = getSettings("settings.json")
    apiKey = settings["ApiKey"]
    postUrl = settings["PostUrl"]
    if not apiKey:
        return
    if not postUrl:
        return
    payload["ApiKey"] = apiKey
    Apps = []
    for item in items:
        if count > 1:
            break
        count += 1
        name = item["name"]
        type = 1
        icon = getIconAsString(item["icons"])
        license = item["license"]
        download_link = getDownloadLink(item["links"])
        download_api_link = getGithubReleaseApiLink(download_link)
        detailsDict = getExtraDetailsFromGithubApi(download_api_link)
        print("name={}".format(name))
        print("\ttype={}".format(type))
        print("\ticon={}".format(icon))
        print("\tlicense={}".format(license))
        print("\tdownload={}".format(download_link))
        print("\tdownload_api={}".format(download_api_link))
        created_at = None
        published_at = None
        tag_name = "0.0.0"
        if detailsDict:
            if 'created_at' in detailsDict:
                created_at = detailsDict['created_at']
                print("\tcreated_at={}".format(created_at))
            if 'published_at' in detailsDict:
                published_at = detailsDict['published_at']
                print("\tpublished_at={}".format(published_at))
            if 'tag_name' in detailsDict:
                tag_name = detailsDict['tag_name']
                print("\tversion={}".format(tag_name))
        app = collections.OrderedDict({"id": 0, "name":name, "type":type, "dateAdded":created_at, "lastUpdated":published_at, "src":download_link, "icon":icon, "currentVersion":tag_name})
        Apps.append(app)
    payload["Apps"] = Apps
    postData(postUrl, payload)

scrap()

    