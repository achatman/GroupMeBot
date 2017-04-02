# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 13:13:05 2017

@author: Andrew
"""

import time
from queue import PriorityQueue

Queue_Node_Types = ["Send_Message","Send_Favorite","Flip_Flag_State"]

class Queue_Node(object):
    def __init__(self,dataDict, timeUntil = 0, **kwargs):
        if "unix_time" in kwargs:
            self.priority = kwargs["unix_time"]
        else:
            self.priority = time.time() + timeUntil
        
        if not isinstance(dataDict,dict):
            raise TypeError("First positional argument must be of type dict.")
        
        self.data = {
            "data": dataDict,
            "created_at": time.time(),
            "unix_stamp": self.priority
        }
        
        if "type" in kwargs:
            if kwargs["type"] in Queue_Node_Types:
                self.data.update({"type":kwargs["type"]})
        
    def getTuple(self):
        return (self.priority,self.data)


import random
import json
d = {
    "fake_data": "hello"
}

q = PriorityQueue()
for i in range(0,10):
    node = Queue_Node(d,random.randrange(1,15000),type = "Send_Message")
    q.put(node.getTuple())

while not q.empty():
    temp = q.get()
    print(json.dumps(temp[1],indent=4))