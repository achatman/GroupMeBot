

from config import setupConfig
setupConfig()

from botObj import Bot
import os
import json
import time

BOTS = []
BOT_CONVERT = {}

with open("bot.config") as r:
    config = json.loads(r.readline())
    for i in range(len(config["bot_ids"])):
        BOTS.append(Bot(config["bot_ids"][i]))
        BOT_CONVERT.update({config["group_ids"][i] : i})

def convertSecs(secs):
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

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

lastModified = os.path.getmtime("actions.json") - 1
actions = []
loop_counter = 1200 #Starts high to create output immediately
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
        bot = BOTS[BOT_CONVERT[g["group_id"]]]
        if int(g["unix_time"]) < time.time():
            if g["type"] == "text":
                if not bot.quiet_switch:
                    bot.sendText(g["message"])
                    print("Message sent.")
            if g["type"] == "flag":
                if g["switch"] == "--quiet":
                    bot.quiet_switch = bool(g["direction"])
                if g["switch"] == "--swear":
                    bot.swear_switch = bool(g["direction"])
                print(g['switch'],g["direction"])
            if g["type"] == "pass":
                if bot.swear_switch:
                    bot.sendText(swearSuggestion(g["message"]))
                    print("Cleaned message.")
            if g["type"] == "status":
                out = "Actions Executed: %s\n" % actions_executed
                out += "Actions Pending: %s\n" % (len(actions)-1) #-1 to ignore this action
                if g["data"]["verbosity"] > 0:
                    out += "Running since: %s (UTC)\n" % time.asctime(time.localtime(g["data"]["started"]))
                    out += "Total Runtime: %s\n" % convertSecs(time.time() - g["data"]["started"])
                    out += "Up Time: %s\n" % convertSecs(g["data"]["upTime"])
                    out += "Down Time: %s\n" % convertSecs(g["data"]["downTime"])
                    out += "Up Time Fraction: %s\n" % (g["data"]["upTime"] / (g["data"]["upTime"] + g["data"]["downTime"]))
                if g["data"]["verbosity"] > 1:
                    out += "Current ID: %s\n" % g["data"]["id"]
                    out += "Reconnect in: %s\n" % g["data"]["reconnect_in"]
                    out += "Reconnect at: %s (UTC)\n" % time.asctime(time.localtime(g["data"]["reconnect_at"]))
                    out += "Last Connected at: %s (UTC)\n" % time.asctime(time.localtime(g["data"]["lastConnected"]))
                if g["data"]["verbosity"] > 2:
                    out += "Message Type Counts:\n"
                    for h in g["data"]["message_counts"]:
                        out += "**%s: %d\n" % (h,g["data"]["message_counts"][h])
                bot.sendText(out)
                print("Status Sent.")
            actions_executed+=1
            actions.remove(g)
    loop_counter+=1
    if loop_counter > 60:
        print(time.ctime(),"Actions Executed: " + str(actions_executed),"Actions Pending: " + str(len(actions)), sep='; ')
        loop_counter = 0
    time.sleep(2)
