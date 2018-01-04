def getPageHtmlSourceCode(url):
    try:
        import urllib2

        request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "http://thewebsite.com",
                "Connection": "keep-alive"
        }

        request = urllib2.Request(url, headers = request_headers)
        return urllib2.urlopen(request).read()
    except:
        return "error"

def inputUrl():
    while(1):
        url = raw_input("Enter the name example(Salena_Gomez) : ")
	url = "https://en.wikipedia.org/wiki/" + url
	htmlSourceCode = getPageHtmlSourceCode(url);
        if htmlSourceCode !="error":
            return htmlSourceCode
        print("\nCouldn't connect to web, please check the url entered or try again later\n")
        
def crawlPage(htmlSourceCode):
	end = 0
	start = htmlSourceCode.find('<span class="fn">',end)
	imgUrlStart = htmlSourceCode.find('srcset',start)
	imgUrlEnd = htmlSourceCode.find('.jpg ',imgUrlStart+8)
	return htmlSourceCode[imgUrlStart+8:imgUrlEnd+4]

def lookUp():
	while(1):
		htmlSourceCode = inputUrl()
		imageLink = crawlPage(htmlSourceCode)
		imageLink = "https:" + imageLink
		print(imageLink)
		

lookUp();

