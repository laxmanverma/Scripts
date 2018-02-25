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

def getData(content):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the order keys are added
    mappedData["identifier"] = "cosmopolitanFrontPage"
    mappedData["like"] = "NULL"
    end = 0
    start = content.find('href="', end)
    end = content.find('"',start+6)
    fullStoryUrl = content[start+6:end]
    mappedData["fullStoryUrl"] = "http://www.cosmopolitan.com" + fullStoryUrl

    start = content.find('data-src="', end)
    end = content.find('"',start+10) #or find upto .jpg?
    imgUrl = content[start+10:end]
    mappedData["imgUrl"] = imgUrl

    start = content.find('class="full-item-metadata">', end)
    start = content.find('">',start+27)
    end = content.find('</a>',start+2)
    category = content[start+2:end]
    for code in htmlCodes:
    	category = category.replace(code[1], code[0])
    mappedData["category"] = category

    start = content.find('class="full-item-content">', end)
    start = content.find('">',start+26)
    end = content.find('</a>',start+2)
    title = content[start+2:end]
    for code in htmlCodes:
    	title = title.replace(code[1], code[0])
    mappedData["title"] = title

    start = content.find('itemprop="name">', end)
    end = content.find('</a>', start+16)
    author = content[start+16:end]
    mappedData["author"] = author

    return mappedData

def crawlPage(htmlSourceCode):
    end = 0
    data = []
    while (1):
        start = htmlSourceCode.find('class="full-item "',end)
        end = htmlSourceCode.find('class="full-item "',start+1)
        if (start != -1 and end != -1):
            data.append(getData(htmlSourceCode[start:end]))
        else:
            break

    return data

def getCosmopolitanFrontPageData():
    # cosmopolitanFrontPageDataArray = []
    #http://www.cosmopolitan.com/ajax/infiniteload/?id=d50755a3-19da-4033-ba32-379374bf8486&class=CoreModels%5Csections%5CSectionModel&viewset=homepage&page=13
    url = "http://www.cosmopolitan.com/"
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    cosmopolitanFrontPageDataArray = crawlPage(htmlSourceCode)

    return cosmopolitanFrontPageDataArray

def main():
    cosmopolitanFrontPageData = getCosmopolitanFrontPageData()
    data = {}
    data["frontPage"] = cosmopolitanFrontPageData
    # data = mensXpData + maximData
    # shuffle(data)
    # data = {**maximData, **mensXpData}   #to merge two dictionaries
    # print(json.dumps(data))
    writeToFirebase(json.dumps(data),"Cosmopolitan", "FrontPage")

main()
