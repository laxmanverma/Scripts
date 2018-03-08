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
  "apiKey": "AAAAqerRwI4:APA91bFEBAoQbWPTmBgZF5btDwCzuLu-mv3bV4KW68_lBq8DP62R00WKYWkvgR_wvRHSPgEJZ4MqqdDW4c0_XrqRKt1204OPE1Ym2Osk2z9j8qiDVjg7I1c9_Igkh5CA0hXWPiLwT9hp",
  "authDomain": "instafeedplus.firebaseapp.com",
  "databaseURL": "https://instafeedplus.firebaseio.com",
  "storageBucket": "instafeedplus.appspot.com"
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

def crawlPage(htmlSourceCode):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    mappedData["identifier"] = "hashToday"
    end = 0
    start = htmlSourceCode.find('data-title="',end)
    end = htmlSourceCode.find('"',start+12)
    title = htmlSourceCode[start+12:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title
    start = htmlSourceCode.find('data-url="',end)
    end = htmlSourceCode.find('"',start+10)
    fullStoryUrl = htmlSourceCode[start+10:end]
    mappedData["fullStoryUrl"] = "https://thehash.today" + fullStoryUrl
    start = htmlSourceCode.find('data-original="',end)
    end = htmlSourceCode.find('"',start+15)
    mappedData["imgUrl"] = htmlSourceCode[start+15:end]
    mappedData["description"] = None
    mappedData["author"] = None
    mappedData["date"] = None
    mappedData["otherLinks"] = []
    mappedData["extraInfo"] = []
    mappedData["category"] = "Trending"
    mappedData["like"] = None
    mappedData["view"] = None
    
    return mappedData

def getData():
    url = "https://thehash.today/"
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    end = 0
    while (1):
        start = htmlSourceCode.find('div class="story "',end)
        end = htmlSourceCode.find('button class="share__button"',start+5)
        if (start != -1 and end != -1):
            dataArray.append(crawlPage(htmlSourceCode[start:end]))
        else:
            break
    # shuffle(dataArray)
    return dataArray

def main():
    hashtodayData = getData()
    data = collections.OrderedDict()
    source = {}
    source["id"] = 1
    source["name"] = "Twitter Trending Feeds"
    data["source"] = source
    navBarLinks = []
    linkData = {}
    linkData["name"] = "Winter Olympics"
    linkData["link"] = "https://thehash.today/story/winter-olympics/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Fashion"
    linkData["link"] = "https://thehash.today/story/popular-fashion/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Travel"
    linkData["link"] = "https://thehash.today/story/travel/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Music"
    linkData["link"] = "https://thehash.today/story/popular-music/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Film"
    linkData["link"] = "https://thehash.today/story/film/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Technology"
    linkData["link"] = "https://thehash.today/story/technology/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Photography"
    linkData["link"] = "https://thehash.today/story/popular-photos/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Science"
    linkData["link"] = "https://thehash.today/story/popular-science/"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "Sports"
    linkData["link"] = "https://thehash.today/story/popular-sport/"
    navBarLinks.append(linkData)
    data["navBarLinks"] = navBarLinks
    data["articles"] = hashtodayData
    # print(json.dumps(data))
    writeToFirebase(json.dumps(data),"trending", "body")

main()