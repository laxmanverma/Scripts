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

def writeToFirebase(data, parent, child, subChild):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child(parent).child(child).child(subChild).set(data)

def dataPreparatorForTrending():
    mappedData = collections.OrderedDict()
    mappedData["title"] = "I'm actually always looking for the good news."
    mappedData["color"] = "testing"
    mappedData["image"] = "testing"
    mappedData["date"] = "puglet"
    mappedData["author"] = "testing"
    mappedData["description"] = "testing"
    mappedData["link"] = "testing"
    mappedData["icon"] = "testing"
    return mappedData

def dataPreparatorForRelationship():
    mappedData = collections.OrderedDict()
    mappedData["title"] = "I'm actually always looking for the good news."
    mappedData["color"] = "testing"
    mappedData["image"] = "testing"
    mappedData["date"] = "puglet"
    mappedData["author"] = "testing"
    mappedData["description"] = "testing"
    mappedData["link"] = "testing"
    mappedData["icon"] = "testing"
    return mappedData

def main():
    data = dataPreparatorForTrending()
    writeToFirebase(data, "Misc", "storiesUI", "trending")
    data = dataPreparatorForRelationship()
    writeToFirebase(data, "Misc", "storiesUI", "relationship")

main()
