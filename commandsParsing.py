# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:39:59 2017

@author: Andrew
"""

import json
import random
import time

def respondHelp():
    return """Here is a list of commands I respond to: 
             -h, --help
             |        Get a list of commands.
             -q, --quote [PATTERN]
             |        Get a random professor quote.""";
        
def respondQuote(message):
    if "--quote" in message:
        pattern = "--quote"
    else:
        pattern = "-q"
    arr = message.split()
    prof = arr[min(arr.index(pattern)+1,len(arr)-1)]
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
        return quotesOptions[random.randrange(0,len(quotesOptions))] + " --" + attribute
    else:
        index = random.randrange(0,len(quotesJSON))
        return quotesJSON[index]["Text"] + " --" + quotesJSON[index]["Prof"]

def respondShutUp(message):
    if "--shutup" in message:
        pattern = "--shutup"
    else:
        pattern = "-su"
    arr = message.split()
    try:
        secs = int(arr[min(arr.index(pattern)+1,len(arr)-1)])
    except ValueError:
        secs = 60
    time.sleep(min(secs,3600))
    return "I was quiet for %s seconds."%secs



def parseText(message):
    if "--help" in message or "-h" in message:
        return respondHelp();
    if "--quote" in message or "-q" in message:
        return respondQuote(message)
    if "--shutup" in message or "-su" in message:
        return respondShutUp(message)
    return None
        