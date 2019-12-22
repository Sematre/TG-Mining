import base64
import uuid
from io import StringIO
import gzip
import json
import requests
import time
from datetime import datetime

class TimeTable:
    def __init__(self, date, url):
        self.date = date
        self.url = url

class DSBMobile:
    args = {}

    def __init__(self, username, password):
        self.args["UserId"] = username
        self.args["UserPw"] = password
        self.args["Language"] = "de"

        self.args["Device"] = "Nexus 4"
        self.args["AppId"] = str(uuid.uuid4())
        self.args["AppVersion"] = "2.5.9"
        self.args["OsVersion"] = "27 8.1.0"

        self.args["PushId"] = ""
        self.args["BundleId"] = "de.heinekingmedia.dsbmobile"

    def getTimeTables(self):
        data = self.pullData()
        if data["Resultcode"] is not 0:
            raise Exception(data["ResultStatusInfo"])

        objects = []
        for jsonObject in self.findJsonObjectByTitle(self.findJsonObjectByTitle(data["ResultMenuItems"], "Inhalte")["Childs"], "Pläne")["Root"]["Childs"]:
            objects.append(TimeTable(jsonObject["Date"], jsonObject["Childs"][0]["Detail"]))

        return objects

    def pullData(self):
        headers = {}
        headers["User-Agent"] = "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 4 Build/OPM7.181205.001)"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Type"] = "application/json;charset=utf-8"
        response = requests.post("https://www.dsbmobile.de/JsonHandler.ashx/GetData", headers=headers, data=self.packageArgs()).json()
        return json.loads(gzip.decompress(base64.b64decode(response["d"])).decode("UTF-8"))

    def findJsonObjectByTitle(self, sourceArray, title):
        for element in sourceArray:
            if "Title" in element:
                if element["Title"].lower() == title.lower():
                    return element

    def packageArgs(self):
        date = datetime.fromtimestamp(int(time.time())).strftime("%a %b %d %Y %H:%M:%S")
        self.args["Date"] = date
        self.args["LastDate"] = date

        innerArgs = {"Data": base64.b64encode(gzip.compress(bytes(json.dumps(self.args), "UTF-8"))).decode('ascii'), "DataType": 1}
        return json.dumps(dict({"req": innerArgs}))