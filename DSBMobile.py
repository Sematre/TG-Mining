import requests
import json

class TimeTable:
    def __init__(self, isHtml, date, groupName, title, url):
        self.isHtml = isHtml
        self.date = date
        self.groupName = groupName
        self.title = title
        self.url = url

class News:
    def __init__(self, headLine, date, id, imageUrl, shortMessage, wholeMessage):
        self.headLine = headLine
        self.date = date
        self.id = id
        self.imageUrl = imageUrl
        self.shortMessage = shortMessage
        self.wholeMessage = wholeMessage

class DSBMobile:
    def __init__(self, username, password):
        response = "[" + requests.get("https://iphone.dsbcontrol.de/iPhoneService.svc/DSB/authid/" + username + "/" + password).text + "]"
        self.key = json.loads(response)[0]
        if self.key == "00000000-0000-0000-0000-000000000000":
            raise ValueError("Wrong username or password")
    
    def getTimeTables(self):
        objects = []
        for jsonObject in json.loads(requests.get("https://iphone.dsbcontrol.de/iPhoneService.svc/DSB/timetables/" + self.key).text):
            objects.append(TimeTable(jsonObject["ishtml"], jsonObject["timetabledate"], jsonObject["timetablegroupname"], jsonObject["timetabletitle"], jsonObject["timetableurl"]))
        
        return objects
    
    def getNews(self):
        objects = []
        for jsonObject in json.loads(requests.get("https://iphone.dsbcontrol.de/iPhoneService.svc/DSB/news/" + self.key).text):
            objects.append(News(jsonObject["headline"], jsonObject["newsdate"], jsonObject["newsid"], jsonObject["newsimageurl"], jsonObject["shortmessage"], jsonObject["wholemessage"]))
        
        return objects