import types
import twc.dsmarshal as twc
import twccommon.Log as twccommon
dsm = twc.dsmarshal

def getInterestList(type, updateCache = 0):
    if not updateCache:
        
        try:
            return _interestList[type]
        except KeyError:
            pass

    
    
    try:
        key = 'interestlist.%s' % (type,)
        il = dsm.configGet(key)
        twccommon.Log.info('%s interest list loaded from data-store: %s' % (type, str(il)))
        _interestList[type] = il
        return il
    except KeyError:
        return []



def isInterested(**kw):
    for key, val in kw.items():
        if not isInterestedItem(key, val):
            return 0
        
    
    return 1


def isInterestedItem(ilType, value):
    if type(value) != types.ListType:
        value = [
            value]
    
    il = getInterestList(ilType)
    for val in value:
        if val not in il:
            return 0
        
    
    return 1

_interestList = { }
