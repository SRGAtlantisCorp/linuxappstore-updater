from bs4 import BeautifulSoup
import requests

def getIconAsString(icons):
    if icons and len(icons) > 0:
        return icons[0]
    else:
        return None

def getDownloadLink(data):
    if (data):
        length = len(data)
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

def getDateFields(api_url):
    if api_url:
        r = requests.get(api_url)
        json = r.json()
        for item in json:
            prerelease = item["prerelease"]
            if not prerelease:
                created_at = item["created_at"]
                published_at = item["published_at"]
                return {'created_at':created_at, 'published_at':published_at }

r = requests.get('https://appimage.github.io/feed.json')
json = r.json()
items = json["items"]
for item in items:
    name = item["name"]
    type = 1
    icon = getIconAsString(item["icons"])
    license = item["license"]
    download_link = getDownloadLink(item["links"])
    download_api_link = getGithubReleaseApiLink(download_link)
    dateDict = getDateFields(download_api_link)
    print("name={}\n".format(name))
    print("\ttype={}\n".format(type))
    print("\ticon={}\n".format(icon))
    print("\tlicense={}\n".format(license))
    print("\tdownload={}".format(download_link))
    print("\tdownload_api={}".format(download_api_link))
    if dateDict:
        if 'created_at' in dateDict:
            created_at = dateDict['created_at']
            print("\tcreated_at={}".format(created_at))
        if 'published_at' in dateDict:
            published_at = dateDict['published_at']
            print("\tpublished_at={}".format(published_at))
    