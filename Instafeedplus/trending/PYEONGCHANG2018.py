import urllib.request
from urllib.request import urlopen
import json
import pyrebase
import schedule
import time
import collections
from random import shuffle

htmlCodes = (
            ("'", '&#039;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;'),
            ("'", '\u2018'),
            ("'", '\u2019'),
            (" ", '&nbsp;'),
            ("", '\n'),
            ("", '\t')
            )

config = {
  "apiKey": "**********",
  "authDomain": "******.firebaseapp.com",
  "databaseURL": "https://*********.firebaseio.com",
  "storageBucket": "*************.appspot.com"
}

def writeToFirebase(data, parent, child):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child(parent).child(child).set(data)

def getPageHtmlSourceCode(url):
    try:
        request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "http://thewebsite.com",
                "Connection": "keep-alive"
        }

        resp = urllib.request.Request(url, headers = request_headers)
        resp = urlopen(resp).read()                 #.decode(resp.headers.get_content_charset())
        return resp
    except:
        return "error"

def inputUrl(url):
    htmlSourceCode = getPageHtmlSourceCode(url);
    if htmlSourceCode !="error":
        return htmlSourceCode
    print("\nCouldn't connect to web, please check the url entered or try again later\n")

def crawlPage(content):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    mappedData["identifier"] = content["topic"]["name"]
    title = content["title"]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title
    mappedData["imgUrl"] = content["thumb"]["desktop"]
    fullStoryUrl = content["url"]
    mappedData["fullStoryUrl"] = "https://www.olympic.org" + fullStoryUrl
    mappedData["description"] = None
    mappedData["author"] = None
    mappedData["date"] = content["date"]
    mappedData["otherLinks"] = []
    mappedData["extraInfo"] = []
    mappedData["category"] = "Games"
    mappedData["like"] = None
    mappedData["view"] = None
    
    return mappedData

def getData():
    url = "https://www.olympic.org/ajaxscript/loadmoreoverviewnews/%7B2A9F605D-4E26-4264-8AF8-9EC0973058FD%7D/40/0"
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    htmlSourceCode = json.loads(htmlSourceCode)
    for content in htmlSourceCode["content"]:
        dataArray.append(crawlPage(content))

    return dataArray

def main():
    pyeongChangNewsData = getData()
    data = collections.OrderedDict()
    source = {}
    source["id"] = 1
    source["name"] = "PYEONGCHANG 2018"
    data["source"] = source
    navBarLinks = []
    linkData = {}
    linkData["name"] = "Watch Live"
    linkData["link"] = "https://www.olympicchannel.com/en/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Schedule & Results"
    linkData["link"] = "https://www.olympic.org/pyeongchang-2018/results/en/general/competition-schedule.htm"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Photos"
    linkData["link"] = "https://www.olympic.org/photos"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Medalists"
    linkData["link"] = "https://www.olympic.org/pyeongchang-2018/results/en/general/multi-medallists.htm"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Museum"
    linkData["link"] = "https://www.olympic.org/museum"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Shop"
    linkData["link"] = "http://shop.olympic.org/en"
    navBarLinks.append(linkData)
    data["navBarLinks"] = navBarLinks
    data["articles"] = pyeongChangNewsData
    # print(json.dumps(data))
    writeToFirebase(json.dumps(data),"trending", "body")

main()
