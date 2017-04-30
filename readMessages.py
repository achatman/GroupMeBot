# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:20:44 2017

@author: Andrew
"""

from config import setupConfig

setupConfig()

from longpoll import handshake
from longpoll import userchannel
from longpoll import poll
from commandsParsing import parseText


import time
import json
import requests

with open("bot.config") as r:
    config = json.loads(r.readline())
    groups = config["group_ids"]

with open("rude.json", mode = 'r') as r:
    rude = json.loads(r.readline())

ID = 1
message_counts = {}

def countMessage(message_type, count = 1):
    if message_type in message_counts:
        message_counts[message_type] += count
    else:
        message_counts.update({message_type : count})

def connect():
    global ID;
    sig = handshake(ID)
    ID += 1
    userchannel(ID,sig)
    ID += 1
    return sig;
    
def process(response):
    
    #alert = response["data"]["alert"]
    groupid = response["data"]["subject"]["group_id"]
    senderid= response["data"]["subject"]["sender_id"]
    messageText = response["data"]["subject"]["text"]
    senderType = response["data"]["subject"]["sender_type"]
    #senderName = response["data"]["subject"]["name"]
    
    #Check that the message was in a group that has a bot running
    if groupid not in groups:
        print("Message in unmonitored group.")
        countMessage("unmonitored")
        return;
    #Check that the message has text content
    elif messageText == None:
        print("Message with no text content.")
        countMessage("no_text")
        return;
    #Check if message was sent by a bot
    elif senderType == "bot":
        print("Bot Message.")
        countMessage("bot")
        return;
    else:
        countMessage("parsed")

    status = {
        "id" : ID,
        "reconnect_in": reconnect - int(connectTime),
     	 "reconnect_at": reconnect,
        "lastConnected": connectTime,
        "started": startingTime,
        "downTime": errorCount * waitTime,
        "upTime": time.time() - (startingTime + (errorCount * waitTime)),
        "message_counts": message_counts
    }
    parseText(messageText, status, senderid)

sig = connect()
startingTime = int(time.time())
connectTime = int(time.time())
errorCount= 0
reconnect = time.time() + 300
waitTime = 30

while True:
    try:
        if int(time.time()) > reconnect:
            sig = connect()
            connectTime = int(time.time())
            reconnect = connectTime + 300
        print("Polling %d..." % ID, end = ' ')
        ret = poll(ID,sig)
        ID += 1
        timeout = ret[0]["advice"]["timeout"]
        reconnect = connectTime + int(timeout) / 1000
        if ret[1]["data"]["type"] == "line.create":
            process(ret[1])
        elif ret[1]["data"]["type"] == "ping":
            print("No event. Reconnect in: %s"%(reconnect - connectTime), flush = True)
            countMessage("no_event")
        else:
            rettype = ret[1]["data"]["type"]
            print("Response Type", rettype)
            countMessage(rettype)
            
    except requests.exceptions.ConnectionError:
        print("Connection Error.", "Reconnecting in", end = ' ', flush = True)
        errorCount += 1
        ID += 1
        for i in range(0,3):
            print("%s seconds..."%int(waitTime - (i*waitTime/3)),end = ' ', flush = True)
            #time.sleep(waitTime/3)
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