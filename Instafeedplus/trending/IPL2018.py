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
            ("", '\t'),
            ("", '            ')
            )

config = {
  "apiKey": "************",
  "authDomain": "*******.firebaseapp.com",
  "databaseURL": "https://**********.firebaseio.com",
  "storageBucket": "***********.appspot.com"
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
    mappedData["identifier"] = "IPL2018"
    title = content['title']
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title
    mappedData["fullStoryUrl"] = "https://www.iplt20.com/news/" + str(content['id'])
    mappedData["imgUrl"] = content['imageUrl']
    mappedData["description"] = None
    mappedData["author"] = None
    mappedData["date"] = None
    mappedData["otherLinks"] = []
    mappedData["extraInfo"] = []
    mappedData["category"] = "Trending"
    mappedData["like"] = None
    mappedData["view"] = None
    
    return mappedData

def getData(url):
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    # print(htmlSourceCode)
    dataArray = []
    htmlSourceCode = json.loads(htmlSourceCode)
    for content in htmlSourceCode["content"]:
        dataArray.append(crawlPage(content))

    # shuffle(dataArray)
    return dataArray

def crawlPageTopFeeds(htmlSourceCode):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    mappedData["identifier"] = "IPL2018"
    end = 0
    start = htmlSourceCode.find('href="',end)
    end = htmlSourceCode.find('"',start+6)
    fullStoryUrl = htmlSourceCode[start+6:end]
    mappedData["fullStoryUrl"] = "https://www.iplt20.com" + fullStoryUrl

    start = htmlSourceCode.find('img class="small-media-item__img" src="',end)
    end = htmlSourceCode.find('"',start+39)
    imgUrl = htmlSourceCode[start+39:end]
    for code in htmlCodes:
        imgUrl = imgUrl.replace(code[1], code[0])
    mappedData["imgUrl"] = imgUrl

    start = htmlSourceCode.find('class="small-media-item__heading"',end)
    end = htmlSourceCode.find('</h1>',start+34)
    title = htmlSourceCode[start+34:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title

    mappedData["description"] = None
    mappedData["author"] = None
    mappedData["date"] = None
    mappedData["otherLinks"] = []
    mappedData["extraInfo"] = []
    mappedData["category"] = "Trending"
    mappedData["like"] = None
    mappedData["view"] = None
    
    return mappedData

def getData1():
    url = "https://www.iplt20.com/"
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    end = 0
    while (1):
        start = htmlSourceCode.find('<li class="u-no-margin-bottom ',end)
        end = htmlSourceCode.find('class="small-media-item__meta"',start+5)
        if (start != -1 and end != -1):
            dataArray.append(crawlPageTopFeeds(htmlSourceCode[start:end]))
            # print(json.dumps(dataArray))
            # exit()
        else:
            break
    # shuffle(dataArray)
    return dataArray

def main():
    hashtodayData = []
    topFeed = getData1()

    for feed in topFeed:
        hashtodayData.append(feed)

    for i in range(0,10):
        url = "https://api.platform.iplt20.com/content/ipl/text/EN/?page=" + str(i) + "&pageSize=8&tagNames=news&references=&playlistTypeRestriction="
        dataArray = getData(url)
        for data in dataArray:
          hashtodayData.append(data)

    data = collections.OrderedDict()
    source = {}
    source["id"] = 1
    source["name"] = "IPL 2018"
    data["source"] = source
    navBarLinks = []
    linkData = {}
    linkData["name"] = "Points Table"
    linkData["link"] = "https://www.iplt20.com/stats/2018"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Social"
    linkData["link"] = "https://www.iplt20.com/social/ipl-on-social"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Videos"
    linkData["link"] = "https://www.iplt20.com/video"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Results"
    linkData["link"] = "https://www.iplt20.com/results"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Schedule"
    linkData["link"] = "https://www.iplt20.com/schedule"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "All Time Records"
    linkData["link"] = "https://www.iplt20.com/stats/all-time"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Auction"
    linkData["link"] = "https://www.iplt20.com/auction/2018"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Teams"
    linkData["link"] = "https://www.iplt20.com/teams"
    navBarLinks.append(linkData)
    data["navBarLinks"] = navBarLinks
    data["articles"] = hashtodayData
    # print(json.dumps(data))
    print("Completed")
    writeToFirebase(json.dumps(data),"trending", "body")

# main()
schedule.every(6).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
