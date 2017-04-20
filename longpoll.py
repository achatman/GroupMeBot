# -*- coding: utf-8 -*-

import requests
import json
import time

fayeURL = "https://push.groupme.com/faye"
userID = "15434777"
botPlayID = "29961146"
with open("token.txt") as r:
    tok = r.readline()

def handshake(ID):
    handshake = [
        {
            "channel": "/meta/handshake",
            "version": "1.0",
            "supportedConnectionTypes": ["long-polling"],
            "id": str(ID)
        }
    ]
    r = requests.post(fayeURL, json = handshake)
    if(r.status_code != 200):
        print("Handshake: ",r.status_code, r.reason)
        print(json.dumps(r.json(),sort_keys=True, indent = 4))
    #returns signature
    #print(json.dumps(r.json(),indent = 4))
    return r.json()[0]["clientId"]
    

def userchannel(ID,sig):
    userChannel = [
        {
            "channel": "/meta/subscribe",
            "clientId" :sig,
            "subscription": "/user/" + userID,
            "id": str(ID),
            "ext":
                {
                    "access_token": tok,
                    "timestamp": int(time.time())
                }
        }
    ]
    r = requests.post(fayeURL, json = userChannel)
    #print(json.dumps(r.json(),indent = 4))
    if(r.status_code != 200):
        print("User Channel: ",r.status_code, r.reason)
        print(json.dumps(r.json(),sort_keys=True, indent = 4))

def poll(ID,sig):
    poll = [
        {
            "channel": "/meta/connect",
            "clientId": sig,
            "connectionType": "long-polling",
            "id": str(ID)
        }
    ]
    r = requests.post(fayeURL, json = poll)
    if (r.status_code != 200):
        print("Poll: ",r.status_code, r.reason)
        print(json.dumps(r.json(),sort_keys=True, indent = 4))
    #print(json.dumps(r.json(), indent = 4))
    return r.json()