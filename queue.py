# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:36:17 2017

@author: Andrew
"""

from queue import PriorityQueue


q = PriorityQueue()

q.put((5,"5"))
q.put((9,"9"))
q.put((7,"7"))
q.put((3,"3"))
q.put((1,"1"))
q.put((3,"3"))
q.put((6,"6"))


while not q.empty():
    print(q.get()[1])