import urllib.request
from urllib.request import urlopen
import json
import pyrebase
import schedule
import time
import collections
from random import shuffle

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

def main():
    url = "https://www.google.co.in/search?ei=966SWt3RJsjSvAT8qIz4Dg&dcr=0&yv=2&newwindow=1&tbm=isch&q=wallpaper&chips=q:wallpaper,g_2:anime&vet=10ahUKEwidqaiyi8HZAhVIKY8KHXwUA-8QuT0I7QEoAQ.966SWt3RJsjSvAT8qIz4Dg.i&ved=0ahUKEwidqaiyi8HZAhVIKY8KHXwUA-8QuT0I7QEoAQ&ijn=2&start=200&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc"
    data = inputUrl(url)
    print(data)

main()
