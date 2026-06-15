'''Grouping of all the corba interfaces.
'''
import CosNaming

def getNamePath(str):
    return map((lambda e: CosNaming.NameComponent(e, '')), str.split('.'))


def setOrb(orb):
    global _orb
    _orb = orb


def getOrb():
    return _orb

_orb = None
