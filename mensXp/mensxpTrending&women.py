import urllib.request
from urllib.request import urlopen
import json
import pyrebase
import schedule
import time
import collections
from random import shuffle      

config = {
  "apiKey": "****",
  "authDomain": "****.firebaseapp.com",
  "databaseURL": "https://*****.firebaseio.com",
  "storageBucket": "****.appspot.com"
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
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the oreder keys are added
    end = 0
    start = content.find('title="', end)
    end = content.find('"',start+7)
    category = content[start+7:end]
    mappedData["category"] = category

    start = content.find('class="count"', end)
    if (start != -1):
        end = content.find('<i', start+14)
        like = content[start+15:end]
        mappedData["like"] = like
    
    start = content.find('href="', end)
    end = content.find('"', start+6)
    fullStoryUrl = content[start+6:end]
    mappedData["fullStoryUrl"] = fullStoryUrl

    start = content.find('title="', end)
    end = content.find('"', start+7)
    title = content[start+7:end]
    mappedData["title"] = title
    
    start = content.find('<img class="lazy" src="', end)
    end = content.find('" data-original', start+23)
    imgUrl = content[start+23:end]
    mappedData["imgUrl"] = imgUrl

    return mappedData
        
def crawlPage(htmlSourceCode):
    end = 0
    data = []
    while (1):
        start = htmlSourceCode.find('<figure>',end)
        end = htmlSourceCode.find('</figure>',start)
        if (start != -1 and end != -1):
            data.append(getData(htmlSourceCode[start:end]))
        else:
            break

    return data

def main():
	#url = "https://www.mensxp.com/trending.html"
    url = "https://www.mensxp.com/feed/section_latest/188?offset=0&limit=100"   # find url by htmlSourceCode.find('data-next-page-url="') and replace value of offset by 0 and limit by 100
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')     #for converting bytes to string
    data = crawlPage(htmlSourceCode)
    shuffle(data)                                       #for shuffling the list
    trending = {}
    trending["trending"] = data
    print(json.dumps(trending))
    writeToFirebase(json.dumps(trending),"MensXp","Trending")

    #url = "https://www.mensxp.com/women.html"
    url = "https://www.mensxp.com/feed/section_latest/395?offset=0&limit=100"
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')
    womenData = crawlPage(htmlSourceCode)
    shuffle(womenData)
    women = {}
    women["women"] = womenData
    print(json.dumps(women))
    writeToFirebase(json.dumps(women),"MensXp","Women")


main()
# schedule.every(15).seconds.do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

"""schedule.every(1).minutes.do(main)
schedule.every().hour.do(main)
schedule.every().day.at("10:30").do(main)
schedule.every().monday.do(main)
schedule.every().wednesday.at("13:15").do(main)"""
