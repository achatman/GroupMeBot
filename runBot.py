

from botObj import Bot
import os
import json
import time

BOT = Bot("703271301450305b8b94947068")

def swearSuggestion(message):
    with open("rude.json") as r:
        rude = json.loads(r.readline())
    arr = message.split()
    clean = message
    for g in arr:
        if g.lower() in rude:
            index = clean.find(g)
            clean = clean[:index] + rude[g.lower()] + clean[index + len(g):]
    return clean

lastModified = os.path.getmtime("actions.json")
actions = []
loop_counter = 120 #Starts high to create output immediately
actions_executed = 0
while(True):
    if os.path.getmtime("actions.json") > lastModified:
        lines = 0
        with open("actions.json", mode = 'r') as r:
            for line in r:
                actions.append(json.loads(line))
                lines += 1
        w = open("actions.json", mode = 'w')
        w.close()
        print("Added %s action(s). Pending: %s."%(lines,len(actions)))
        lastModified = os.path.getmtime("actions.json")
    for g in actions:
        if int(g["unix_time"]) < time.time():
            if g["type"] == "text":
                if not BOT.shutup_switch:
                    BOT.sendText(g["message"])
                    print("Message sent.")
            if g["type"] == "flag":
                if g["switch"] == "--shutup":
                    BOT.shutup_switch = bool(g["direction"])
                if g["switch"] == "--swear":
                    BOT.swear_switch = bool(g["direction"])
                print(g['switch'],g["direction"])
            if g["type"] == "pass":
                if BOT.swear_switch:
                    BOT.sendText(swearSuggestion(g["message"]))
                    print("Cleaned message.")
            if g["type"] == "status":
                out = g["message"]
                out += "Actions Executed: %s\n"%actions_executed
                out += "Actions Pending: %s\n"%len(actions-1) #-1 to ignore this action
                BOT.sendText(out)
                print("Status Sent.")
            actions_executed+=1
            actions.remove(g)
    loop_counter+=1
    if loop_counter > 60:
        print(time.ctime(),"Actions Executed: " + str(actions_executed),"Actions Pending: " + str(len(actions)), sep='; ')
        loop_counter = 0
    time.sleep(2)
