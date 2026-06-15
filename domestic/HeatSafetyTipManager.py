'''
Provides a way to read in the Heat Safety Tips File and insert them into 
a list.  Will also return the correct tupple to product requesting data.
'''
import os
_tipList = []
_index = 0

def init(fileName):
    ns = { }
    ns['addTip'] = addTip
    execfile(fileName, ns, ns)


def addTip(title, tip):
    _tipList.append((title, tip))


def getTip():
    global _index
    str = _tipList[_index]
    _index = (_index + 1) % len(_tipList)
    return str

