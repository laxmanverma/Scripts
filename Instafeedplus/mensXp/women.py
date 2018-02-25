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
            (" ", '&nbsp;')
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
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the oreder keys are added
    mappedData["identifier"] = "MensXp"
    mappedData["author"] = "NULL"
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
    else:
        mappedData["like"] = "NULL"

    start = content.find('href="', end)
    end = content.find('"', start+6)
    fullStoryUrl = content[start+6:end]
    mappedData["fullStoryUrl"] = fullStoryUrl

    start = content.find('title="', end)
    start = content.find('">',start)
    end = content.find(' </span>', start+3)
    title = content[start+3:end]
    for code in htmlCodes:
    	title = title.replace(code[1], code[0])
    mappedData["title"] = title

    start = content.find('data-original="', end)
    end = content.find('"', start+23)
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

def parseMaximData(content):
    mappedData = collections.OrderedDict()
    mappedData["identifier"] = "MaximWomen"
    end = 0
    start = content.find('<img ',end)
    start = content.find('src="',start+4)
    end = content.find('"',start+5)
    img = content[start+5:end]
    mappedData["imgUrl"] = img

    start = content.find('<a class="m-card--header"',end)
    start = content.find('href="',start)
    end = content.find('"',start+6)
    fullStoryUrl = content[start+6:end]
    mappedData["fullStoryUrl"] = "https://www.maxim.com" + fullStoryUrl

    start = content.find('<h2',end)
    start = content.find('>',start+3)
    end = content.find('</',start+2)
    title = content[start+1:end]
    for code in htmlCodes:
        title = title.replace(code[1], code[0])

    mappedData["title"] = title
    mappedData["category"] = "Maxim Women"
    mappedData["like"] = "NULL"
    mappedData["author"] = "NULL"

    return mappedData

def crawlMaximPage(htmlSourceCode):
	end = 0
	data = []
	while (1):
		start = htmlSourceCode.find('<article',end)
		end = htmlSourceCode.find('</article>',start)
		if (start != -1 and end != -1):
			data.append(parseMaximData(htmlSourceCode[start:end]))
		else:
			break

	return data

def getMaximData():
	url = "https://www.maxim.com/tag/women"
	htmlSourceCode = inputUrl(url)
	htmlSourceCode = htmlSourceCode.decode('utf-8')
	maximWomen = crawlMaximPage(htmlSourceCode)

	return maximWomen

def getMensXpWomenData():
    womenDataArray = []
    womenData = []
    offset = 0
    while offset < 1:
        #url = "https://www.mensxp.com/women.html"
        url = "https://www.mensxp.com/feed/section_latest/395?offset=" + str(offset) + "&limit=100"
        htmlSourceCode = inputUrl(url)
        htmlSourceCode = htmlSourceCode.decode('utf-8')
        womenData.append(crawlPage(htmlSourceCode))
        offset += 100
    for data in womenData:
        for datum in data:
            womenDataArray.append(datum)

    return womenDataArray

def main():
    maximData = getMaximData()
    mensXpData = getMensXpWomenData()
    data = mensXpData + maximData
    shuffle(data)
    # data = {**maximData, **mensXpData}   #to merge two dictionaries
    # print(json.dumps(data))
    writeToFirebase(json.dumps(data),"Mix", "Women")

main()
