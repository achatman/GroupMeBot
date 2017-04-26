# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:39:59 2017

@author: Andrew
"""

import json
import random
import time
import re
import datetime
import pytz

NAME = "Sarah"
with open("options.json") as r:
    opts = json.loads(r.readline())

months = {
    1 : ["Jan", 31],
    2 : ["Feb", 28],
    3 : ["Mar", 31],
    4 : ["Apr", 30],
    5 : ["May", 31],
    6 : ["Jun", 30],
    7 : ["Jul", 31],
    8 : ["Aug", 31],
    9 : ["Sep", 30],
    10: ["Oct", 31],
    11: ["Nov", 30],
    12: ["Dec", 31]
}

'''
Action types:
    text - text to send to a group
    flag - switch a flag on or off
    pass - non-command message
    status - responding with status
'''
def writeAction(data):
    with open("actions.json", mode = 'a') as a:
        a.write(json.dumps(data) + "\n")
    print("Wrote action with flag: " + data["type"])

def writeText(message,Deltat=0):
    data = {
        "type": "text",
        "message": message,
        "unix_time": time.time() + Deltat
    }
    writeAction(data)

def switchFlag(flag,Deltat):
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

def sendStatus(message):
    data = {
        "type": "status",
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

def respondHelp(message):
    if "--help" in message:
        pattern = "--help"
    else:
        pattern = "-h"
    arg = getArguments(message,pattern,1)[0]
    bulletChar = "*"
    out = 'Here is a list of commands I respond to:\n'
    opt = ''
    for g in opts:
        if arg == opts[g]["long"] or arg == opts[g]["short"]:
            opt = g
            break
    if opt != '' and opt != 'Help':
        out = "Help page for: " + opt + '\n'
        flags = bulletChar.ljust(3) + opts[g]["short"] + ','
        flags = flags.ljust(7)
        flags += opts[g]["long"]
        for g in range(len(opts[opt]["options"])):
            flags += " [%s=%s]"%(opts[opt]["options"][g]["name"],
                                 opts[opt]["options"][g]["default"])
        out += flags + '\n'
        out += (bulletChar*2).ljust(6) + opts[opt]["desc"]
        for h in range(0,len(opts[opt]["options"])):
            out += '\n'
            out += (bulletChar*3).ljust(9) + opts[opt]["options"][h]["name"] + ' - ' + opts[opt]["options"][h]["desc"]
    else:
        out = "Here is a list of commands I respond to:" + '\n'
        for g in opts:
            flags = bulletChar.ljust(3) + opts[g]["short"] + ','
            flags = flags.ljust(7)
            flags += opts[g]["long"]
            for h in range(0,len(opts[g]["options"])):
                flags += " [%s=%s]"%(opts[g]["options"][h]["name"], opts[g]["options"][h]["default"])
            out += flags + '\n'

    writeText(out)

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

'''
Accepted formats:
Example:
2017-03-14T15:30:45

Deltat - 120 [seconds]
UNIX time - 1489505445

yyyy-mm-ddThh:mm:ss
* ^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d$
* 2017-03-14T15:30:45
* Exact time
yyyy-mm-ddThh:mm
* ^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$
* 2017-03-14T15:30
* Exact time
yyyy-mm-dd
* ^\d\d\d\d-\d\d-\d\d$
* 2017-03-14
* Noon on given day
yyyy
* ^\d\d\d\d$
* 2017
* Noon on January 1
mm-dd
* ^\d\d-\d\d$
* 03-14
* Noon on next occurance of given date
hh:mm
* ^\d\d:\d\d$
* 15:30
* Next occurance of given time
hh:mm:ss
* ^\d\d:\d\d:\d\d$
* 15:30:45
* Next occurance of given time
'''
def respondReminder(message):
    if "--remindme" in message:
        pattern = "--remindme"
    else:
        pattern = "-rm"
    arg = getArguments(message,pattern,1)[0]
    if re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d$",arg):
        match = re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d$",arg).string
        date = [int(match[0:4]),   int(match[5:7]),   int(match[8:10]),
                int(match[11:13]), int(match[14:16]), int(match[17:19])]
    elif re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$",arg):
        match = re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d$",arg).string
        date = [int(match[0:4]),   int(match[5:7]),   int(match[8:10]),
                int(match[11:13]), int(match[14:16]), 0]
    elif re.search(r"^\d\d\d\d-\d\d-\d\d$",arg):
        match = re.search(r"^\d\d\d\d-\d\d-\d\d$",arg).string
        date = [int(match[0:4]), int(match[5:7]), int(match[8:10]),
                12, 0, 0]
    elif re.search(r"^\d\d\d\d$",arg):
        match = re.search(r"^\d\d\d\d$",arg).string
        date = [int(match), 1, 1, 12, 0, 0]
    elif re.search(r"^\d\d-\d\d$",arg):
        match = re.search(r"^\d\d-\d\d$",arg).string
        date = [-1, int(match[0:2]), int(match[3:5]), 12, 0, 0]
    elif re.search(r"^\d\d:\d\d$",arg):
        match = re.search(r"^\d\d:\d\d$",arg).string
        date = [-1, -1, -1, int(match[0:2]), int(match[3:5]), 0]
    elif re.search(r"^\d\d:\d\d:\d\d$",arg):
        match = re.search(r"^\d\d:\d\d:\d\d$",arg).string
        date = [-1, -1, -1, int(match[0:2]), int(match[3:5]), int(match[6:8])]
    else:
        return;

    #yyyy, MM, dd, hh, mm, ss
    #   0,  1,  2,  3,  4,  5

    #Set implicit parameters
    localtime = time.localtime(time.time())
    if date[0] == -1:
        date[0] = localtime[0]
    if date[1] == -1:
        date[1] = localtime[1]
    if date[2] == -1:
        date[2] = localtime[2]

    #Check ranges
    if date[5] < 0 or date[5] > 60:
        return
    if date[4] < 0 or date[4] > 60:
        return
    if date[3] < 0 or date[3] > 24:
        return

    if date[0] < localtime[0]:
        return;
    if date[1] < 0 or date[1] > 12:
        return;
    if date[2] < 0 or date[2] > months[date[1]][1]:
        return;

    #Check if time is passed
    remindTime = datetime.datetime(date[0],date[1],date[2],date[3],date[4],date[5])
    if remindTime.timestamp() < time.time():
        return;

    writeText("Reminder set for %s, %s seconds from now."%(arg, remindTime.timestamp() - time.time()))
    writeText("This is a reminder for %s"%arg, remindTime.timestamp() - time.time())


def respondStatus(message, ID, reconnect, lastConnected):
    if "--status" in message:
        pattern = "--status"
    else:
        pattern = "-s"
    arg = getArguments(message,pattern,1)[0]
    try:
        verbosity = int(arg)
    except ValueError:
        verbosity = 0
    if verbosity == 0:
        out = ""
    elif verbosity == 1:
        out = """Current ID: %s
                 Last Connected: %s
                 Reconnect in: %s
              """%(ID, lastConnected, reconnect)
    sendStatus(out)

def parseText(message):
    if NAME in message:
        if "--help" in message.split() or "-h" in message.split():
            respondHelp(message);
        if "--quote" in message.split() or "-q" in message.split():
            respondQuote(message)
        if "--shutup" in message.split() or "-su" in message.split():
            respondShutUp(message)
        if "--alive" in message.split() or "-a" in message.split():
            respondAlive()
        if "--swear" in message.split() or "-sw" in message.split():
            respondSwearFilter(message)
        if "--remindme" in message.split() or "-rm" in message.split():
            respondReminder(message)
    else:
        passMessage(message)