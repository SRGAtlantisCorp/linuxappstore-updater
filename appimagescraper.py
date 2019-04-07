import json
import requests
import datetime
import dateutil.parser

def getSettings(file_name):    
    try:
        try:
            with open(file_name) as json_file:
                settings = {}
                data = json.load(json_file)
                apiKey = data["ApiKey"]
                if not apiKey:
                    raise ValueError("Could not read ApiKey from settings.")

                postUrl = data["PostUrl"]
                if not postUrl:
                    raise ValueError("Could not read PostUrl from settings.")

                settings["ApiKey"] = apiKey            
                settings["PostUrl"] = postUrl   
                return settings
        except:
            raise ValueError("Could not open file={}".format(file_name))     
    except ValueError as e:
        print(e)

def getIconAsString(icons):
    if icons and len(icons) > 0:
        return icons[0]
    else:
        return ''

def getDownloadLink(data):
    if (data):
        for item in data:
            type = item["type"]
            if type == "Download":
                download_link = item["url"]
                return download_link
    else:
        return ''

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

def getAppImageFeed(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        print("Failed to retrieve AppImage feed.")

def scrap():
    feedJson = getAppImageFeed('https://appimage.github.io/feed.json')
    if feedJson is None:
        return

    items = feedJson["items"]
    count = 0

    settings = getSettings("settings.json")
    if settings is None:
        return

    apiKey = settings["ApiKey"]
    if not apiKey:
        return

    postUrl = settings["PostUrl"]
    if not postUrl:
        return

    payload = {}
    payload["ApiKey"] = apiKey
    Apps = []
    for item in items:
        if count > 1:
            break
        count += 1

        name = item["name"]

        if not name:
            continue

        icon = getIconAsString(item["icons"])

        license = item["license"]
        download_link = getDownloadLink(item["links"])
        if not download_link:
            print("{} does not have a download link".format(name))
            continue

        download_api_link = getGithubReleaseApiLink(download_link)
        detailsDict = getExtraDetailsFromGithubApi(download_api_link)

        print("name={}".format(name))
        print("\ttype={}".format(1))
        print("\ticon={}".format(icon))
        print("\tlicense={}".format(license))
        print("\tdownload={}".format(download_link))
        print("\tdownload_api={}".format(download_api_link))

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
        else:
            created_at_time = datetime.datetime.now()
            created_at = created_at_time.strftime("%Y-%m-%dT%H:%M:%S")
            published_at_time = datetime.datetime.now()
            published_at = published_at_time.strftime("%Y-%m-%dT%H:%M:%S")

        app = {"id": 0, "name":name, "type":1, "dateAdded":created_at, "lastUpdated":published_at, "src":download_link, "icon":icon, "currentVersion":tag_name}
        Apps.append(app)
    payload["Apps"] = Apps
    postData(postUrl, payload)

scrap()

    