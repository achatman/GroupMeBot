# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:20:44 2017

@author: Andrew
"""

from longpoll import handshake
from longpoll import userchannel
from longpoll import poll
from commandsParsing import parseText

import time
import json
import requests


GROUP_ID = "29961146" #"20505137"
AVATAR_URL = "https://i.groupme.com/1920x1080.jpeg.6141b043a4844c3584ad2ef2db520a99"

with open("rude.json", mode = 'r') as r:
    rude = json.loads(r.readline())

ID = 1

def connect():
    global ID;
    sig = handshake(ID)
    print("Connected")
    ID += 1
    userchannel(ID,sig)
    print("Subscribed to Channel")
    ID += 1
    return sig;
    
def process(response):
    messageType = response["data"]["type"]
    if messageType != "line.create":
        print("Type: " + messageType)
        return;
    
    #alert = response["data"]["alert"]
    #groupid = response["data"]["subject"]["group_id"]
    #senderid= response["data"]["subject"]["sender_id"]
    messageText = response["data"]["subject"]["text"]
    senderType = response["data"]["subject"]["sender_type"]
    #senderName = response["data"]["subject"]["name"]
    
    if senderType != "bot":
        status = {
            "id" : ID,
            "reconnect_in": reconnect - int(time.time() - connectTime),
        	 "reconnect_at": reconnect,
            "lastConnected": connectTime,
            "started": startingTime,
            "downTime": errorCount * waitTime,
            "upTime": time.time() - startingTime - (errorCount * waitTime)
        }
        parseText(messageText, status)

sig = connect()
startingTime = int(time.time())
connectTime = int(time.time())
errorCount= 0
reconnect = 300
waitTime = 30
while True:
    try:
        if int(time.time()) > connectTime + reconnect:
            sig = connect()
            connectTime = int(time.time())
            reconnect = 300
        print("Polling...")
        ret = poll(ID,sig)
        ID += 1
        timeout = ret[0]["advice"]["timeout"]
        reconnect = int(timeout) / 1000
        if len(ret[1]["data"]) > 1:
            process(ret[1])
        else:
            print("No event. Reconnect in: %s"%(reconnect - int(time.time() - connectTime)))
    except requests.exceptions.ConnectionError:
        print("Connection Error.", "Reconnecting in", end = ' ', flush = True)
        errorCount += 1
        for i in range(0,3):
            print("%s seconds..."%int(waitTime - (i*waitTime/3)),end = ' ', flush = True)
            time.sleep(waitTime/3)
        print('')
    


''' OLD CODE -still here in case I forgot something
def connect():
    global ID;
    sig = handshake(ID)
    ID+=1
    userchannel(ID,sig)
    ID+=1
    print("Connected")
    return sig

def waitForMessage():
    global ID;
    sig = connect()
    lastConnected = int(time.time())
    while True:
        if ID > 5000:
            u = "ID exceeded max value (max: 5000, ID: %s).\n Total elapsed time: %s."(ID,int(time.time())-startTime)
            print(u)
            return None
        if int(time.time()) - lastConnected > 2700:
            sig = connect()
            lastConnected = int(time.time())
        ret = poll(ID,sig)
        ID+=1
        if ret != None:
            print(json.dumps(ret, indent = 4))
            return ret
        else:
            print("Timeout. ID: ", ID)

def respond(message):
    if message["data"]["type"] != "line.create":
        print(message["data"]["type"])
        return;
    #groupid = message["data"]["subject"]["group_id"]
    
    #senderid = message["data"]["subject"]["sender_id"]
    #messageTimems = float(message["data"]["subject"]["created_at"])
    #messageTime = datetime.datetime.fromtimestamp(messageTimems)
    #senderName = message["data"]["subject"]["name"]
    senderType = message["data"]["subject"]["sender_type"]
    
    messageText = message["data"]["subject"]["text"]
    if not senderType == "bot":
        parseText(messageText)

waitTime = 30
while True:
    try:
        ret = waitForMessage()
        if ret == None:
            break;
        else:
            respond(ret)
    except requests.exceptions.ConnectionError:
        print("Connection Error.", "Reconnecting in", end = ' ', flush = True)
        for i in range(0,3):
            print("%s seconds..."%int(waitTime - (i*waitTime/3)),end = ' ', flush = True)
            time.sleep(waitTime/3)
        print('')
'''