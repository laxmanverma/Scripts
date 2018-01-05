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
	url = "http://www.4ono.com/cbse-12th-science-previous-year-question-papers-pdf-201617/"
	htmlSourceCode = getPageHtmlSourceCode(url);
        if htmlSourceCode !="error":
            return htmlSourceCode
        print("\nCouldn't connect to web, please check the url entered or try again later\n")
        
def crawlPage(htmlSourceCode):
	start = 0
        while(1):
		subjectNameStart = htmlSourceCode.find('<h2 id="',start)
		if subjectNameStart<0:
			break
		subjectNameEnd = htmlSourceCode.find('"',subjectNameStart+8)
		subjectName = htmlSourceCode[subjectNameStart+8:subjectNameEnd-1]
		#my_file = open("output.txt", "a")
		#my_file.write(subjectName + '\n')
		#my_file.close()
		#print(subjectName)
		newSubSection = htmlSourceCode.find('<h2 id="',subjectNameEnd)
		subSectionEnd = subjectNameEnd
		while(subSectionEnd<newSubSection):
			stateStart = htmlSourceCode.find('<p><strong>',subjectNameEnd)
			stateEnd = htmlSourceCode.find('</strong>',stateStart+11)
			state = htmlSourceCode[stateStart+11:stateEnd]
			subjectNameEnd = stateEnd
			if subSectionEnd>newSubSection:
				break
			#my_file = open("output.txt", "a")
			#my_file.write(state + '\n')
			#my_file.close()
			newStateSection = htmlSourceCode.find('<p><strong>',stateEnd+7)
			stateSectionEnd = stateEnd
			while(1):
				pdfLinkStart = htmlSourceCode.find('<a href="',stateEnd)
				subSectionEnd = pdfLinkStart
				pdfLinkEnd = htmlSourceCode.find('.pdf">',pdfLinkStart+9)
				pdfLink = htmlSourceCode[pdfLinkStart+9:pdfLinkEnd+4]
				yearEnd = htmlSourceCode.find("</a>",pdfLinkEnd+4)
				year = htmlSourceCode[pdfLinkEnd+6:yearEnd]
				stateEnd = yearEnd
				stateSectionEnd = yearEnd
				pdfName = subjectName+'-'+state+'-'+year+'.pdf'
				import urllib
				urllib.urlretrieve(pdfLink,pdfName)
				if stateSectionEnd>newStateSection:
					break
				#my_file = open("output.txt", "a")
				#my_file.write(year + '\n')
				#my_file.write(pdfLink + '\n')
				#my_file.close()
				#print(pdfLink)
				#print(year)
		start = subjectNameEnd	

def lookUp():
		htmlSourceCode = inputUrl()
		crawlPage(htmlSourceCode)
		

lookUp();
