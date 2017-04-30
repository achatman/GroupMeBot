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
import requests
from lxml import html

NAME = "Sarah"
with open("options.json") as r:
    opts = json.loads(r.readline())

with open("bible.json") as r:
    bible = json.loads(r.readline())

with open("bot.config") as r:
    config = json.loads(r.readline())
    weather_key = config["weather_key"]

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

def sendStatus(metadata):
    data = {
        "type": "status",
        "data": metadata,
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
    args = getArguments(message,pattern,2)
    prof = args[0]
    try:
        num = int(args[1])
    except ValueError:
        num = 1
    num = min(num, 100)
    with open("profQuotes.json",encoding = 'utf-8',mode = 'r') as r:
        file = json.loads(r.readline())
    quotesJSON = file["Quotes"]
    quotesOptions = []
    out = ''
    for i in range(0,len(quotesJSON)):
        if prof.lower() in quotesJSON[i]["Prof"].lower():
            quotesOptions.append(quotesJSON[i])
    added = []
    if len(quotesOptions) > 0:
        for i in range(num):
            if len(out) > 900:
                writeText(out)
                out = ''
            index = random.randrange(0,len(quotesOptions))
            text = quotesOptions[index]["Text"]
            att = quotesOptions[index]["Prof"]
            if text not in added:
                out += text + ' --' + att + '\n'
                added.append(text)
    else:
        for i in range(num):
            if len(out) > 900:
                writeText(out)
                out = ''
            index = random.randrange(0,len(quotesJSON))
            text = quotesJSON[index]["Text"]
            att =  quotesJSON[index]["Prof"]
            if text not in added:
                out +=  text + " --" + att + '\n'
                added.append(text)
    writeText(out)

def respondQuiet(message):
    if "--quiet" in message:
        pattern = "--quiet"
    else:
        pattern = "-qu"
    arg = getArguments(message,pattern,1)[0]
    try:
        secs = int(arg)
    except ValueError:
        secs = 60
    switchFlag("--quiet",secs)

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


def respondStatus(message, metadata):
    if "--status" in message:
        pattern = "--status"
    else:
        pattern = "-s"
    arg = getArguments(message,pattern,1)[0]
    try:
        verbosity = int(arg)
    except ValueError:
        verbosity = 0
    verbosity = max(0,verbosity)
    metadata.update({"verbosity":verbosity})
    sendStatus(metadata)

def respondEvang():
    replacements = {
        "Jesus" : "Mouse Jesus",        "saints" : "murine saints",     "godliness" : "mousiness",
        "God" : "The Big Cheese",       "Jews" : "Rats",                "Jew" : "Rat",
        "Romans": "Cats",               "Roman" : "Cat",                "Father": "Great Gouda",
        "kiss": "sniff",                "Peace": "Cheese",              "Simon": "Salamander Simon",
        "Peter": "Peter Pig",           "Andrew": "Aardwolf Andrew",    "Philip": "Pheasant Philip",
        "Barnabas": "Barnabas Baboon",  "Lord": "Alpha",                "Rabbi": "Alpha Rat",
        "Matthew": "Matthew Monkey",    "John" : "Jaguar John",         "Mark" : "Moose Mark",
        "Luke" : "Leopard Luke",        "Lamb": "Crumb",                "lamb": "crumb",
        "angel": "curd",                "Angel": "Curd",                "priest": "fromager",
        "Priest": "Fromager"
    }    
    
    versesarr = []
    for g in bible:
        for h in range(len(bible[g]["Chapters"])):
            for i in range(len(bible[g]["Chapters"][h])):
                if "Jesus" in bible[g]["Chapters"][h][i]:
                    versesarr.append(bible[g]["Chapters"][h][i])
    verse = versesarr[random.randrange(0,len(versesarr))]
    for g in bible:
        for h in range(len(bible[g]["Chapters"])):
            for i in range(len(bible[g]["Chapters"][h])):
                if verse == bible[g]["Chapters"][h][i]:
                    address = "%s %d:%d" % (bible[g]["book_name"], h, i)
    
    #Make replacements
    i = 0
    while i < len(verse):
        j = i
        while j < len(verse):
            if verse[i:j] in replacements:
                length = len(replacements[verse[i:j]])
                verse = verse[:i] + replacements[verse[i:j]] + verse[j:]
                i += length
                break
            j += 1
        i += 1
    
    
    verse += '\n' + address
    writeText(verse)
    
def respondWeather():
    url = "http://api.wunderground.com/api/" + weather_key + "/conditions/q/IA/Ames.json"
    r = requests.get(url)
    response = json.loads(r.text)["current_observation"]
    out = "--Current Weather in Ames, IA--\n"
    out += "Weather: %s\n" % response["weather"]
    out += "Temperature: %s\n" % response["temperature_string"]
    out += "Humidity: %s\n" % response["relative_humidity"]
    out += "Wind: %d mph (%d kph) %s\n" % (response["wind_mph"],response["wind_kph"],response["wind_dir"])
    out += "Windchill: %s\n" % response["windchill_string"]
    writeText(out)

def respondShakespeare():
    url = "http://www.pangloss.com/seidel/Shaker/index.html?"
    r = requests.get(url)
    page = r.text
    #Parsing manually, because the source html is shit
    key1 = '<font size="+2">\n'
    key2 = '</font>'
    i1 = page.find(key1)
    i2 = page.find(key2)
    content = page[i1 + len(key1) : i2]
    writeText(content)

def respondHoroscope(message):
    if "--horoscope" in message:
        pattern = "--horoscope"
    else:
        pattern = "-hor"
    arg = getArguments(message,pattern,1)[0]
    hors = ["Aries", "Taurus", "Gemini",   "Sagittarius",
            "Leo",   "Virgo",  "Cancer",   "Capricorn",
            "Libra", "Pisces", "Aquarius", "Scorpio"]
    sign = ''
    for g in hors:
        if arg.lower() in g.lower():
            sign = g
    
    if sign == '' or arg == '':
        sign = hors[random.randrange(0,len(hors))]
    
    #Get Horoscope
    url = "https://www.astrology.com/horoscope/daily/" + sign.lower() + ".html"
    r = requests.get(url)
    page = html.document_fromstring(r.text)
    findclass = page.find_class("page-horoscope-text")
    #I can't be bothered to do any error handling on this right now
    #so I'll just assume that this always works.
    #This isn't the worst assumption, since this website probably won't
    #change anytime soon.
    horoscope = findclass[0].text_content()
    horoscope = "Horoscope for %s:\n" % sign     + horoscope
    
    writeText(horoscope)
    
def checkSender(senderid):
    if senderid == "29861221":
        arr = ["1.60934 kilometers",        "1609.34 meters",           "160934 centimeters",
               "1.609E6 millimeters",       "1760 yards","5280 feet",   "63360 inches",
               "0.868976 nautical miles",   "880 fathoms",              "0.333 leagues",
               "80 chains",                 "320 rods",                 "2.526E-4 Earth Radii",
               "1.076E-8 AU",               "1.701E-13 light years",    "5.216E-14 parsecs",
               "1.146E-26 Hubble lengths"]
        writeText("Miles = %s" % arr[random.randrange(0,len(arr))])

def parseText(message, metadata, sender):
    if NAME in message:
        arr = message.split()
        if "--help" in arr or "-h" in arr:
            respondHelp(message);
        if "--quote" in arr or "-q" in arr:
            respondQuote(message)
        if "--quiet" in arr or "-qu" in arr:
            respondQuiet(message)
        if "--alive" in arr or "-a" in arr:
            respondAlive()
        if "--swear" in arr or "-sw" in arr:
            respondSwearFilter(message)
        if "--remindme" in arr or "-rm" in arr:
            respondReminder(message)
        if "--status" in arr or "-s" in arr:
            respondStatus(message, metadata)
        if "--evangelize" in arr or "-evang" in arr:
            respondEvang()
        if "--weather" in arr or "-w" in arr:
            respondWeather()
        if "--shakespeare" in arr or "-shake" in arr:
            respondShakespeare()
        if "--horoscope" in arr or "-hor" in arr:
            respondHoroscope(message)
        checkSender(sender)
    else:
        passMessage(message)
