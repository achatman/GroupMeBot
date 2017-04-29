# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:44:45 2017

@author: Andrew
"""

import os.path
import json

configPath = "bot.config"

def setupConfig():
    #Check if config file already exists
    if os.path.isfile("bot.config"):
        print("Config file already exists.")
        check = ''
        while True:
            check = input("Would you like to use the existing config file? (y/n)")
            if check == 'y' or check == 'n':
                break;
            else:
                print("Please enter y or n.")
        if check == 'y':
            print("The existing config file will be used.")
            return;
            
    #Default Values:
    token = ''
    userid = ''
    group_ids = []
    bot_ids = []
    log_bot_id = ''
    log_group_id = ''
    commands = {}
    susers = []
    weather_key = ''
    
    #Get Token
    print("You will need to enter your GroupMe API token.")
    print("You can find your API token at https://dev.groupme.com")
    go = True
    while go:
        token = input("Enter your API token here:")
        print("You will be unable to access the GroupMe API with an invalid token.")
        print("You entered %s" % token)
        while True:
            check = input("Are you sure this is your token? (y/n)")
            if check == 'y':
                go = False
                break;
            elif check == 'n':
                break;
            else:
                print("Please enter y or n.")
    
    print()
    
    #Get user ID
    print("You will need to enter your GroupMe user ID.")
    go = True
    while go:
        userid = input("Enter your user ID here:")
        while True:
            check = input("Are you sure this is your user ID? (y/n)")
            if check == 'y':
                go = False
                break;
            elif check == 'n':
                break;
            else:
                print("Please enter y or n.")
    
    
    print()
    
    #Group IDs
    print("Now you need to enter group ID numbers and bot IDs for the bots you want to operate.")
    print("Bot IDs and their corresponding group IDs can be found at https://dev.groupme.com/bots.")
    go = True
    while go:
        botid = input("Enter a bot ID here:")
        groupid = input("Enter the corresponding group ID here:")
        while True:
            check = input("Are you sure these IDs are accurate? (y/n)")
            if check == 'y':
                group_ids.append(groupid)
                bot_ids.append(botid)
                break;
            elif check == 'n':
                break;
            else:
                print("Please enter y or n.")
        while True:
            check = input("Would you like to enter another bot? (y/n)")
            if check == 'y':
                break;
            elif check == 'n':
                go = False
                break;
            else:
                print("Please enter y or n.")
    
    print()    
    
    #Get log group ID
    print("Now you can choose to enter a log bot and group ID.")
    print("If you choose to do so, in addition to the normal log file,")
    print("all log messages will also be sent to the log group.")
    
    log = False
    while True:
        check = input("Would you like to have a log group? (y/n)")
        if check == 'y':
            log = True
            break;
        elif check == 'n':
            break;
        else:
            print("Please enter y or n.")
    
    if log:
        go = True
        while go:
            log_bot_id = input("Please enter the log bot ID here:")
            log_group_id = input("Please enter the log group ID here:")
            while True:
                check = input("Are you sure these IDs are accurate? (y/n)")
                if check == 'y':
                    go = False
                    break;
                elif check == 'n':
                    break;
                else:
                    print("Please enter y or n.")
            
    print()
    
    #Get Allowed Commands
    with open("options.json", mode = 'r') as r:
        options = json.loads(r.readline())
    
        
    
    print("Now you will be able to choose which commands you want your bots to respond to.")
    for g in options:
        print()
        print("Option:",g)
        print("Long flag:", options[g]["long"], ", Short flag:", options[g]["short"])
        print(options[g]["desc"])
        for h in range(0,len(options[g]["options"])):
            print("[%s=%s]" % (options[g]["options"][h]["name"], options[g]["options"][h]["default"]))
            print("    ", options[g]["options"][h]["desc"])
        
        print()
        while True:
            check = input("Would you like to enable this option? (y/n)")
            if check == 'y':
                commands.update({g : True})
                break;
            elif check == 'n':
                commands.update({g : False})
                break;
            else:
                print("Please enter y or n.")
        
    print()
    #Check if su command is included
    #For now, this is always True
        
    su = True
    
    
    if su == True:
        print("You have included at least one super user restricted command.")
        print("You will now be able to choose which users are allowed to use these commands.")
        go = True
        while go:
            userid = input("Enter a user ID to have super user privileges here:")
            while True:
                check = input("Are you sure this ID is accurate? (y/n)")
                if check == 'y':
                    susers.append(userid)
                    break;
                elif check == 'n':
                    break;
                else:
                    print("Please enter y or n.")
            while True:
                check = input("Would you like to enter another super user? (y/n)")
                if check == 'y':
                    break;
                elif check == 'n':
                    go = False
                    break;
                else:
                    print("Please enter y or n.")
    
    print()
    
 
    #Get weather key if the weather option is on
    if commands["Weather"]:
        print("You have chosen to use the weather command.")
        print("For this, you will need to enter a Weather Underground API Key.")
        print("You can find your key at https://www.wunderground.com/weather/api")
        go = True
        while go:
            weather_key = input("Enter your weather key here:")
            while True:
                check = input("Are you sure this key is accurate? (y/n)")
                if check == 'y':
                    go = False
                    break;
                elif check == 'n':
                    break;
                else:
                    print("Please enter y or n.")
                    

    output = {}
    output.update({"token" : token})
    output.update({"user_id" : userid})
    output.update({"group_ids" : group_ids})
    output.update({"bot_ids" : bot_ids})
    output.update({"log_group_id" : log_group_id})
    output.update({"log_bot_id" : log_bot_id})
    output.update({"commands" : commands})
    output.update({"susers" : susers})
    output.update({"weather_key" : weather_key})
    
    with open("bot.config", mode = 'w') as config_writer:
        config_writer.write(json.dumps(output))
    
    print()
    print("You have finished the config setup.")
    print("Your chosen options are stored in bot.config.")
    print("If you ever want to change an option, you can rerun this setup or you can edit the bot.config file manually.")
       