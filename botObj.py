# -*- coding: utf-8 -*-

import requests
import json

with open("bot.config") as r:
    config = json.loads(r.readline())
    tok = config["token"]
    
url = "https://api.groupme.com/v3/bots?token=" + tok

class Bot(object):
    def __strTypeCheck(self, arg, argname):
        if not isinstance(arg, str):
            raise TypeError(argname + "field must be of type str.")
    
    def __init__(self,ID):
        self.__strTypeCheck(ID,"ID")
        self.id = ID
        self.url = "https://api.groupme.com/v3/bots/post"
        self.quiet_switch = False
        self.swear_switch = False
        
    def sendText(self,string):
        self.__strTypeCheck(string,"string")
        data = {
                "bot_id": self.id,
                "text"  : string
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Text send failed.")
            print(r.status_code, r.reason)
            print("Problematic text:", string)
            print("Respone text:", r.text)
    
    def sendImage(self,imageURL):
        self.__strTypeCheck(imageURL,"imageURL")
        data = {
                "bot_id": self.id,
                "attachments": [{
                    "type": "image",
                    "url" : imageURL
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Image send failed.")
            print(r.status_code, r.reason)
            print("Image URL: " + imageURL)
            
    def sendLocation(self, lng, lat, name):
        self.__strTypeCheck(lng,"lng")
        self.__strTypeCheck(lat,"lat")
        self.__strTypeCheck(name,"name")
        data = {
                "bot_id": self.id,
                "attachments": [{
                    "type" : "location",
                    "lng"  : lng,
                    "lat"  : lat,
                    "name" : name
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Location send failed.")
            print(r.status_code, r.reason)
            print("Longitude: " + lng)
            print("Latitude: " + lat)
            print("Name: " + name)
    
    def sendText_Image(self,string,imageURL):
        self.__strTypeCheck(string,"string")
        self.__strTypeCheck(imageURL,"imageURL")
        data = {
                "bot_id": self.id,
                "text"  : string,
                "attachments": [{
                    "type": "image",
                    "url" : imageURL
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Text/Image send failed.")
            print(r.status_code, r.reason)
            print("Message text: " + string)
            print("Image URL: " + imageURL)
            
    def sendText_Location(self, string, lng, lat, name):
        self.__strTypeCheck(string,"string")
        self.__strTypeCheck(lng,"lng")
        self.__strTypeCheck(lat,"lat")
        self.__strTypeCheck(name,"name")
        data = {
                "bot_id": self.id,
                "text"  : string,
                "attachments": [{
                    "type" : "location",
                    "lng"  : lng,
                    "lat"  : lat,
                    "name" : name
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Text/Location send failed.")
            print(r.status_code, r.reason)
            print("Message text: " + string)
            print("Longitude: " + lng)
            print("Latitude: " + lat)
            print("Name: " + name)
    
    def sendImage_Location(self, imageURL, lng, lat, name):
        self.__strTypeCheck(imageURL,"imageURL")
        self.__strTypeCheck(lng,"lng")
        self.__strTypeCheck(lat,"lat")
        self.__strTypeCheck(name,"name")
        data = {
                "bot_id": self.id,
                "attachments": [{
                    "type" : "location",
                    "lng"  : lng,
                    "lat"  : lat,
                    "name" : name
                },{
                    "type" : "image",
                    "url"  : imageURL
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Image/Location send failed.")
            print(r.status_code, r.reason)
            print("Image URL: " + imageURL)
            print("Longitude: " + lng)
            print("Latitude: " + lat)
            print("Name: " + name)
            
    def sendText_Image_Location(self, string, imageURL, lng, lat, name):
        self.__strTypeCheck(string,"string")
        self.__strTypeCheck(imageURL,"imageURL")
        self.__strTypeCheck(lng,"lng")
        self.__strTypeCheck(lat,"lat")
        self.__strTypeCheck(name,"name")
        data = {
                "bot_id": self.id,
                "text"  : string,
                "attachments": [{
                    "type" : "location",
                    "lng"  : lng,
                    "lat"  : lat,
                    "name" : name
                },{
                    "type" : "image",
                    "url"  : imageURL
                }]
        }
        r = requests.post(self.url, json = data)
        if not r.status_code == 202:
            print("Text/Image/Location send failed.")
            print(r.status_code, r.reason)
            print("Message text: " + string)
            print("Image URL: " + imageURL)
            print("Longitude: " + lng)
            print("Latitude: " + lat)
            print("Name: " + name)