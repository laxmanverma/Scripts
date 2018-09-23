import urllib.request
from urllib.request import urlopen
import json
import pyrebase
import schedule
import time
import collections
from random import shuffle
import sys

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
            ("'", '&#8216;'),
            ("'", '&#8217;')
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

def crawlPageIndiaExpress(htmlSourceCode):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    source = {}
    source["id"] = 1
    source["name"] = "IndianExpress"
    mappedData["source"] = source
    end = 0
    start = htmlSourceCode.find('class="date"', end)
    end = htmlSourceCode.find('</div>',start+13)
    publishedAt = htmlSourceCode[start+13:end]
    mappedData["publishedAt"] = publishedAt
    mappedData["dateAvailable"] = True
    mappedData["dateFormat"] = "format"

    start = htmlSourceCode.find('img ',end)
    start = htmlSourceCode.find('src="',start)
    start = htmlSourceCode.find('src="',start+5)
    end = htmlSourceCode.find('"',start+5)    
    urlToImage = htmlSourceCode[start+5:end]
    # sys.exit()
    mappedData["urlToImage"] = urlToImage

    start = htmlSourceCode.find('class="title"',end)
    start = htmlSourceCode.find('href="',start+12)
    end = htmlSourceCode.find('"',start+6)
    url = htmlSourceCode[start+6:end]
    mappedData["url"] = url

    start = end
    end = htmlSourceCode.find('</a>',start+6)
    title = htmlSourceCode[start+2:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title

    start = htmlSourceCode.find('<p>',end)
    end = htmlSourceCode.find('</p>',start+6)
    description = htmlSourceCode[start+3:end]
    for code in htmlCodes:
        description = description.replace(code[1], code[0])
    mappedData["description"] = description

    mappedData["author"] = None
    
    return mappedData

def getDataIndiaExpress(url):
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    end = 0
    while (1):
       start = htmlSourceCode.find('div class="articles"',end)
       end = htmlSourceCode.find('div class="articles"',start+5)
       if (start != -1 and end != -1):
        dataArray.append(crawlPageIndiaExpress(htmlSourceCode[start:end]))
       else:
        break
    return dataArray

def crawlPageNDTV(htmlSourceCode):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    end = 0
    if (htmlSourceCode.find('class="new_storylising_img"',end) == -1):
    	source = {}
    	source["id"] = 1
    	source["name"] = "Advertisement"
    	mappedData["source"] = source
    	mappedData["url"] = "https://play.google.com/store/apps/details?id=com.buggyarts.android.cuotos.gaana"
    	mappedData["title"] = "Play your favorite tracks from awesome music app InPLAY"
    	mappedData["urlToImage"] = "https://raw.githubusercontent.com/krmayank911/InPlay/master/inplayfg.png"
    	mappedData["publishedAt"] = "gsd"
    	mappedData["dateAvailable"] = False
    	mappedData["dateFormat"] = "format"
    	mappedData["author"] = "gsd"
    	mappedData["description"] = "A music player application developed for android os. Play your favourite tracks by making new playlists, browse by artists and albums. Compact size, Beautiful design."
    	return mappedData

    source = {}
    source["id"] = 1
    source["name"] = "NDTV"
    mappedData["source"] = source

    start = htmlSourceCode.find('href="',end)
    end = htmlSourceCode.find('"',start+6)
    url = htmlSourceCode[start+6:end]
    mappedData["url"] = url

    start = htmlSourceCode.find('title="', end)
    end = htmlSourceCode.find('">',start+7)
    title = htmlSourceCode[start+7:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title

    start = htmlSourceCode.find('img src="',end)
    end = htmlSourceCode.find('"',start+9)
    urlToImage = htmlSourceCode[start+9:end]
    mappedData["urlToImage"] = urlToImage

    mappedData["publishedAt"] = None
    mappedData["dateAvailable"] = False
    mappedData["dateFormat"] = "format"

    start = htmlSourceCode.find('class="nstory_intro"',end)
    end = htmlSourceCode.find('."</div>',start+22)
    description = htmlSourceCode[start+21:end-11]
    for code in htmlCodes:
        description = description.replace(code[1], code[0])
    mappedData["description"] = description

    mappedData["author"] = None
    
    return mappedData

def getDataNDTV(url):
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    end = htmlSourceCode.find('div class="new_storylising"',0)
    last = htmlSourceCode.find('class="new_pagination"',0)
    while (1):
        start = htmlSourceCode.find('<li>',end)
        end = htmlSourceCode.find('</li>',start+4)
        if (start != -1 and end != -1 and end <= last):
           dataArray.append(crawlPageNDTV(htmlSourceCode[start:end]))
        else:
           break
    return dataArray

def crawlPageIndiatoday(htmlSourceCode):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the orders keys are added
    source = {}
    source["id"] = 1
    source["name"] = "INDIATODAY"
    mappedData["source"] = source
    end = 0
    start = htmlSourceCode.find('img src="',end)
    end = htmlSourceCode.find('"',start+9)    
    urlToImage = htmlSourceCode[start+9:end]
    # print(urlToImage.replace('-170x96', ''))
    mappedData["urlToImage"] = urlToImage.replace('-170x96', '')

    start = htmlSourceCode.find('title="',end)
    start = htmlSourceCode.find('title="',start+1)
    end = htmlSourceCode.find('">',start+7)
    title = htmlSourceCode[start+7:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])
    mappedData["title"] = title

    mappedData["publishedAt"] = None
    mappedData["dateAvailable"] = False
    mappedData["dateFormat"] = "format"


    start = htmlSourceCode.find('href="',end)
    end = htmlSourceCode.find('"',start+6)
    url = htmlSourceCode[start+6:end]
    mappedData["url"] = "https://www.indiatoday.in" + url

    start = htmlSourceCode.find('<p>',end)
    end = htmlSourceCode.find('</p>',start+6)
    description = htmlSourceCode[start+3:end]
    for code in htmlCodes:
        description = description.replace(code[1], code[0])
    mappedData["description"] = description

    mappedData["author"] = None
    
    return mappedData

def getDataIndiatoday(url):
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    dataArray = []
    end = htmlSourceCode.find('div class="catagory-listing"',0)
    last = htmlSourceCode.find('<h2 class="element-invisible">Pages</h2>',end)
    while (1):
        start = htmlSourceCode.find('div class="catagory-listing"',end)
        end = htmlSourceCode.find('div class="catagory-listing"',start+1)
        if (start != -1 and end != -1 and end <= last):
           dataArray.append(crawlPageIndiatoday(htmlSourceCode[start:end]))
        else:
           break
    return dataArray

def main():
    data = collections.OrderedDict()
    articlesArray = []
    #navbar links-------------------------------
    navBarLinks = []
    linkData = {}
    linkData["name"] = "India News"
    linkData["link"] = "#"
    navBarLinks.append(linkData)
    linkData = {}
    linkData["name"] = "World News"
    linkData["link"] = "#"
    navBarLinks.append(linkData)
    data["navBarLinks"] = navBarLinks
    #navbar links ends --------------------------

    # #indianexpress ------------------------------
    url = "http://indianexpress.com/latest-news/"
    indianexpress = getDataIndiaExpress(url)
    articlesArray.append(indianexpress)
    #indianexpress ends ------------------------------

    #indiatoday --------------------------------------
    url = "https://www.indiatoday.in/india?page=0&view_type=list"
    indiatoday1 = getDataIndiatoday(url)
    # articlesArray.append(indiatoday)
    url = "https://www.indiatoday.in/india?page=1&view_type=list"
    indiatoday2 = getDataIndiatoday(url)
    indiatoday = indiatoday1 + indiatoday2
    articlesArray.append(indiatoday)
    #indiatoday ends ------------------------------------

    #ndtv ---------------------------------------
    url = "https://www.ndtv.com/india?pfrom=home-topnavigation"
    ndtv = getDataNDTV(url)
    articlesArray.append(ndtv)
    #ndtv ends ---------------------------------------
    # newsData = ndtv+indiatoday+indianexpress
    # articlesArray.append(ndtv+indiatoday+indianexpress)
    # shuffle(newsData)
    data["articles"] = articlesArray
    # print(json.dumps(data))
    writeToFirebase(json.dumps(data),"newsPoolIndia", "English")

main()
