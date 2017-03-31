# -*- coding: utf-8 -*-

import requests

urlBASE = "https://api.groupme.com/v3/bots?token="

def makeBot(botname,groupid,avatarURL):
    with open("token.txt") as r:
        tok = r.readline()
    
    data = {
        "bot" : {
            "name": botname,
            "group_id": groupid,
            "avatar_url": avatarURL
            }
    }
    r = requests.post(urlBASE + tok, json = data)
    print(r.status_code, r.reason)
    print(r.json())




botname = input("Bot name: ")
groupid = input("Group ID: ")
avatar  = input("Avatar URL: ")
makeBot(botname,groupid,avatar)