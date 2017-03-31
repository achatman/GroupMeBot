# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:20:44 2017

@author: Andrew
"""

from botObj import Bot
from longpoll import handshake
from longpoll import userchannel
from longpoll import poll
from commandsParsing import parseText

import time
import datetime
import json

bot = Bot("703271301450305b8b94947068")
NAME = "Sarah"
GROUP_ID = "29961146" #"20505137"
AVATAR_URL = "https://i.groupme.com/1920x1080.jpeg.6141b043a4844c3584ad2ef2db520a99"


with open("rude.json", mode = 'r') as r:
    rude = json.loads(r.readline())

ID = 1
startTime = int(time.time())

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
            bot.sendText(u)
            return None
        if int(time.time()) - lastConnected > 2700:
            sig = connect()
            lastConnected = int(time.time())
        ret = poll(ID,sig)
        ID+=1
        if ret != None:
            return ret
        else:
            print("Timeout. ID: ", ID)
            
    

def respond(message):
    if message["data"]["type"] != "line.create":
        print(message["data"]["type"])
        return;
    groupid = message["data"]["subject"]["group_id"]
    if groupid != GROUP_ID:
        print("Wrong Group")
        return;    
    
    senderid = message["data"]["subject"]["sender_id"]
    #messageTimems = float(message["data"]["subject"]["created_at"])
    #messageTime = datetime.datetime.fromtimestamp(messageTimems)
    #senderName = message["data"]["subject"]["name"]
    
    if(senderid == "384147"):
        bot.sendText("I am the best bot. Fuck InfoBot")
    
    messageText = message["data"]["subject"]["text"]
    if(NAME in messageText):
        toSend = parseText(messageText)
    else:
        toSend = None
    
    if(toSend != None):
        print(toSend)
        bot.sendText(toSend)

while True:
    ret = waitForMessage()
    if ret == None:
        break;
    else:
        respond(ret)