import urllib.request
from urllib.request import urlopen
import schedule
import time
import collections
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def dataPreparatorForRelationship():
    mappedData = collections.OrderedDict()
    mappedData["label"] = "car"
    mappedData["image_url"] = "testing"
    return mappedData

data = []
data1 = dataPreparatorForRelationship()
data2 = dataPreparatorForRelationship()
data.append(data1)
data.append(data2)

doc_ref = db.collection(u'users').document(u'testing')
doc_ref.set({
    u'url': data
})

print("complete")
