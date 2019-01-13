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
  "apiKey": "*************",
  "authDomain": "******.firebaseapp.com",
  "databaseURL": "https://******.firebaseio.com",
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

def getData(content):
    mappedData = collections.OrderedDict()      #for ordering the dictionary in the oreder keys are added
    mappedData["identifier"] = "mensXp"
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
    mappedData["identifier"] = "maxim"
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
    mappedData["category"] = "Maxim Man"
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
	url = "https://www.maxim.com/tag/maxim-man"
	htmlSourceCode = inputUrl(url)
	htmlSourceCode = htmlSourceCode.decode('utf-8')
	data = crawlMaximPage(htmlSourceCode)
	maximMan = {}
	maximMan["man"] = data
	# print(json.dumps(maximMan))
	writeToFirebase(json.dumps(maximMan),"Maxim","man")

def getHeadingData():
	mappedData = collections.OrderedDict()
	mappedData["title"] = "I'm actually always "
	mappedData["subTitle"] = "looking for the good news."
	mappedData["color"] = "testing"
	mappedData["image"] = "testing"
	mappedData["date"] = "puglet"
	mappedData["author"] = "testing"
	mappedData["description"] = "testing"
	mappedData["link"] = "testing"
	mappedData["icon"] = "testing"
	return mappedData

def main():
	#url = "https://www.mensxp.com/trending.html"
    url = "https://www.mensxp.com/feed/section_latest/188?offset=0&limit=100"   # find url by htmlSourceCode.find('data-next-page-url="') and replace value of offset by 0 and limit by 100
    htmlSourceCode = inputUrl(url)
    htmlSourceCode = htmlSourceCode.decode('utf-8')     #for converting bytes to string
    data = crawlPage(htmlSourceCode)
    #shuffle(data)                                       #for shuffling the list
    trending = {}
    trending["trending"] = data
    trending["heading"] = getHeadingData()
    # print(json.dumps(trending))
    writeToFirebase(json.dumps(trending),"MensXp","Trending")

    # #url = "https://www.mensxp.com/women.html"
    # url = "https://www.mensxp.com/feed/section_latest/395?offset=0&limit=100"
    # htmlSourceCode = inputUrl(url)
    # htmlSourceCode = htmlSourceCode.decode('utf-8')
    # womenData = crawlPage(htmlSourceCode)
    # #shuffle(womenData)
    # women = {}
    # women["women"] = womenData
    # #print(json.dumps(women))
    # writeToFirebase(json.dumps(women),"MensXp","Women")

    relationshipData = []
    relationshipDataArray = []
    offset = 0
    while offset < 1000:
	    url = "https://www.mensxp.com/feed/section_latest/97?offset=" + str(offset) + "&limit=100"
	    htmlSourceCode = inputUrl(url)
	    htmlSourceCode = htmlSourceCode.decode('utf-8')
	    relationshipData.append(crawlPage(htmlSourceCode))
	    offset += 100
    #shuffle(data)
    for data in relationshipData:
        for datum in data:
            relationshipDataArray.append(datum)

    blah = []
    blah.append(relationshipDataArray)
    relationship = {}
    relationship["relationship"] = blah
    relationship["heading"] = getHeadingData()
    #print(json.dumps(relationship))
    writeToFirebase(json.dumps(relationship),"MensXp","Relationship")

    getMaximData()

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
