# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:39:59 2017

@author: Andrew
"""

import json
import random
import time

NAME = "Sarah"

#types: text, flag, pass
def writeAction(data):
    with open("actions.json", mode = 'a') as a:
        a.write(json.dumps(data) + "\n")

def writeText(message,Deltat=0):
    print(message)
    data = {
        "type": "text",
        "message": message,
        "unix_time": time.time() + Deltat
    }
    writeAction(data)

def switchFlag(flag,Deltat):
    print(flag)
    data = {
        "type": "flag",
        "switch": flag,
        "direction": True,
        "unix_time": time.time()
    }
    writeAction(data)
    data = {
        "type": "flag",
        "switch": flag,
        "direction": False,
        "unix_time": time.time() + Deltat
    }
    writeAction(data)

def passMessage(message):
    data = {
        "type": "pass",
        "message": message,
        "unix_time": time.time()
    }
    writeAction(data)

def getArguments(text,pattern,numArgs):
    arr = text.split()
    args = []
    for i in range(0,numArgs):
        args.append( arr[min(arr.index(pattern)+1+i,len(arr)-1)] )
    return args;

def respondHelp():
    writeText( """Here is a list of commands I respond to: 
             -h,  --help
             |        Get a list of commands.
             -q,  --quote [PATTERN='']
             |        Get a random professor quote.
             -su, --shutup [TIME=60]
             |        Turn off all messages for TIME seconds.
             -sw, --swear [TIME=60]
             |        Turn on the swear filter for TIME seconds.""")
        
def respondQuote(message):
    if "--quote" in message:
        pattern = "--quote"
    else:
        pattern = "-q"
    prof = getArguments(message,pattern,1)[0]
    with open("profQuotes.json",encoding = 'utf-8',mode = 'r') as r:
        file = json.loads(r.readline())
    quotesJSON = file["Quotes"]
    quotesOptions = []
    attribute = ''
    for i in range(0,len(quotesJSON)):
        if prof.lower() in quotesJSON[i]["Prof"].lower():
            attribute = quotesJSON[i]["Prof"]
            quotesOptions.append(quotesJSON[i]["Text"])
    if len(quotesOptions) > 0:
        writeText(quotesOptions[random.randrange(0,len(quotesOptions))] + " --" + attribute)
    else:
        index = random.randrange(0,len(quotesJSON))
        writeText(quotesJSON[index]["Text"] + " --" + quotesJSON[index]["Prof"])

def respondShutUp(message):
    if "--shutup" in message:
        pattern = "--shutup"
    else:
        pattern = "-su"
    arg = getArguments(message,pattern,1)[0]
    try:
        secs = int(arg)
    except ValueError:
        secs = 60
    switchFlag("--shutup",secs)

def respondAlive():
    writeText("Still alive.")

def respondSwearFilter(message):
    if "--swear" in message:
        pattern = "--swear"
    else:
        pattern = "-sw"
    arg = getArguments(message,pattern,1)[0]
    try:
        secs = int(arg)
    except ValueError:
        secs = 60
    switchFlag("--swear",secs)

def parseText(message):
    if NAME in message:
        if "--help" in message or "-h" in message:
            respondHelp();
        if "--quote" in message or "-q" in message:
            respondQuote(message)
        if "--shutup" in message or "-su" in message:
            respondShutUp(message)
        if "--alive" in message or "-a" in message:
            respondAlive()
        if "--swear" in message or "-sw" in message:
            respondSwearFilter(message)
    else:
        passMessage(message)