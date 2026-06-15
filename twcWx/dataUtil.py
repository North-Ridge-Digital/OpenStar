import twccommon
import twcWx.SkyCondMapping as sky
import twcWx.TextFcstMapping as txt
import twcWx.IncidentTypeMapping as inc
import twcWx.BackgroundMusicMapping as bkgMusic
import twcWx.PromoMessageMapping as promoMsg
incidentTypeMap = inc.IncidentTypeMapping(1)

def getIncidentType(typeID, mappingFile, default = None):
    result = incidentTypeMap.get(typeID, mappingFile)
    if result == None:
        if default == None:
            result = twccommon.Data(group = '', description = '')
        else:
            result = default
    
    return result

skyCondMap = sky.SkyCondMapping(1)

def formatSkyCondition(iconCode, locale = 'default', default = None):
    result = skyCondMap.get(iconCode, locale)
    if result == None:
        if default == None:
            result = twccommon.Data(iconFile = 'BlankIcon', textModifier = '')
        else:
            result = default
    
    return result


def skyConditionHasPrecip(iconCode):
    data = skyCondMap.get(iconCode, 'Observation')
    if data.precipitation == None:
        return 0
    
    return data.precipitation


def getSkyCondGroup(iconCode):
    data = skyCondMap.get(iconCode, 'ExtendedForecast')
    if data.group == None:
        return 0
    
    return data.group

textFcstMap = txt.TextFcstMapping(1)

def getTextMapping(code, mappingFile, default = None):
    result = textFcstMap.get(code, mappingFile)
    if result == None:
        if default == None:
            result = twccommon.Data(text = '')
        else:
            result = default
    
    return result

bkgMusicMap = bkgMusic.BackgroundMusicMapping(1)

def getBackgroundMusicList(mappingFile):
    result = bkgMusicMap.getList(mappingFile)
    return result

promoMsgMap = promoMsg.PromoMessageMapping(1)

def getPromoMessageList(mappingFile):
    result = promoMsgMap.getList(mappingFile)
    return result


def getPromoMessageAt(mappingFile, index):
    list = promoMsgMap.getList(mappingFile)
    
    try:
        result = promoMsgMap[index]
        return result
    except:
        return promoMsgMap[0]



def validateAttr(obj, attrs):
    for attr in attrs:
        if obj.__dict__.has_key(attr) == 0:
            return None
        
    
    return obj

