import re
import time
import types
import shutil
import twc.dsmarshal as twc
import twc.DataStoreInterface as twc
import twc.InterestList as twc
import twc.MiscCorbaInterface as twc
import twccommon
import twccommon.Log as twccommon
import domestic.BulletinInfo as domestic
import os
import glob
from xml.sax import make_parser, handler
ds = twc.DataStoreInterface
dsm = twc.dsmarshal
BulletinInfo = domestic.BulletinInfo
_ldlIdList = []
CHANNEL_NAME = 'SystemEventChannel'
MAP_ACTIVE_KEY = 'mapcuts.active'
MAP_PENDING_KEY = 'mapcuts.pending'
MAP_FORCE_KEY = 'mapcuts.force'

class IconParserHandler(handler.ContentHandler):
    
    def __init__(self):
        self._data = { }

    
    def startElement(self, name, attrs):
        if name == 'record':
            self._data[(str(attrs.get('wxId')), str(attrs.get('night', '0')))] = (str(attrs.get('wxId')), str(attrs.get('movie')), str(attrs.get('sfx_name')), str(attrs.get('night', '0')))
        



def getTextFcstMultimedia(audioCode):
    sCodeRe = re.compile('S([0-9]{4})([0-9])')
    for audioElement in audioCode.split(':'):
        sCodeMatch = sCodeRe.match(audioElement)
        if sCodeMatch:
            sCode = sCodeMatch.groups()[0]
            sDayPart = sCodeMatch.groups()[1]
            if sDayPart in [
                '2',
                '4']:
                sDayPart = '1'
            else:
                sDayPart = '0'
            
            try:
                sCode = str(int(sCode))
            except ValueError:
                pass

            break
        
    else:
        return (None, None)
    parser = make_parser()
    iconHandler = IconParserHandler()
    parser.setContentHandler(iconHandler)
    parser.parse('/media/mappings/textForecast/AnimatedIcons.xml')
    data = iconHandler._data
    
    try:
        mapping_element = data[(sCode, sDayPart)]
    except KeyError:
        if sDayPart == '1':
            
            try:
                mapping_element = data[(sCode, '0')]
            except KeyError:
                mapping_element = (None, None, None, None)

        else:
            mapping_element = (None, None, None, None)
    except:
        sDayPart == '1'

    return (mapping_element[1], mapping_element[2])


def getBulletinInterestList(ugc):
    cl = getUGCInterestList(ugc, 'county')
    zl = getUGCInterestList(ugc, 'zone')
    return cl + zl


def getUGCInterestList(ugc, type):
    locs = []
    mo = _ugcRegex.search(ugc)
    while mo != None:
        (start, end) = mo.span()
        sl = ugc[start:end]
        ugc = ugc[end:]
        locs.extend(_parseUGCStateList(sl))
        mo = _ugcRegex.search(ugc)
    il = _getInterestList(type)
    locs = filter((lambda e: e in il), locs)
    return locs


def setDailyRec(loc, data, obsTimeT):
    currTemp = getattr(data, 'temp', None)
    if currTemp:
        twccommon.Log.debug('currTemp = %d' % currTemp)
        dailyRec = twc.Data(currHighTemp = currTemp, currLowTemp = currTemp)
        save = 0
        
        try:
            dkey = 'daily.%s.recordTemps' % loc
            dailyRec = dsm.get(dkey)
            if currTemp > dailyRec.currHighTemp:
                save = 1
                dailyRec.currHighTemp = currTemp
            
            if currTemp < dailyRec.currLowTemp:
                save = 1
                dailyRec.currLowTemp = currTemp
        except:
            save = 1

        if save == 1:
            (y, m, d, H, M, S, wd, jd, dst) = time.localtime(obsTimeT)
            midnight = time.mktime((y, m, d + 1, 0, 0, 0, 0, 0, -1))
            dsm.set(dkey, dailyRec, int(midnight))
        
    


def setData(loc, type, data, expiration, update = 0):
    if type == 'obs':
        setDailyRec(loc, data, expiration - 75 * 60)
    
    key = '%s.%s' % (type, str(loc))
    _setData(key, data, expiration, update)
    twccommon.Log.debug('set %s' % (key,))
    if type == 'hdln':
        log_msg = 'set hdln for location %s' % loc
        twccommon.Log.info(log_msg)
        modifiedHeadlines = []
        matchCategories = ((4, 'HURRICANE WIND WATCH', re.compile('HURRICANE WIND WATCH'), 'HURRICANE WATCH'), (3, 'HURRICANE WATCH', re.compile('HURRICANE WATCH'), 'HURRICANE WATCH'), (2, 'HURRICANE WIND WARNING', re.compile('HURRICANE WIND WARNING'), 'HURRICANE WARNING'), (1, 'HURRICANE WARNING', re.compile('HURRICANE WARNING'), 'HURRICANE WARNING'))
        for i in range(len(data.headlines)):
            headline = data.headlines[i]
            compareHeadline = ' '.join(headline.upper().split())
            matchAppender = []
            for v, match, headlineRe, abb in matchCategories:
                if headlineRe.search(compareHeadline):
                    matchAppender = [
                        (v, i, abb, headline)]
                
            
            modifiedHeadlines += matchAppender
        
        modifiedHeadlines.sort()
        if len(modifiedHeadlines) > 0:
            d = twc.Data(header = modifiedHeadlines[0][2], message = modifiedHeadlines[0][3])
            dsm.set('hurricaneStatement', d, expiration)
            ds.commit()
        else:
            
            try:
                dsm.remove('hurricaneStatement')
                ds.commit()
            except KeyError:
                pass

    


def setDaypartData(loc, type, data, validTime, numDayparts, expiration, update = 0):
    (Y, M, D, h, m, s, wday, day, dst) = time.localtime(validTime)
    window = 24 / numDayparts
    h = (h / window) * window
    validTime = time.mktime((Y, M, D, h, 0, 0, wday, day, -1))
    key = '%s.%s.%d' % (type, str(loc), validTime)
    _setData(key, data, expiration, update)
    twccommon.Log.debug('set %s' % (key,))


def setBulletin(loc, data, expiration):
    setBulletins([
        (loc, data, expiration)])


def setBulletins(blist):
    setlist = []
    for loc, data, expiration in blist:
        info = BulletinInfo.getBulletinProperties(data.pil, data.pilExt)
        il = _getInterestList('county')
        if loc in il[1:]:
            if not (info.multicountied):
                continue
            
        
        data.county = loc
        data.expiration = expiration
        groupOverride = getattr(info, 'groupOverride', 0)
        if groupOverride == 1 and data.group != '':
            group = data.group
            _addGroup(group)
        else:
            group = info.group
        setlist.append((loc, group))
        which = '%s.%s' % (loc, group)
        key = 'bulletin.' + which
        dsm.set(key, data, expiration, 0)
        key = 'bulletin.lastIssue.%s' % data.pil
        dsm.set(key, data.issueTime, 0, 0)
        key = 'bulletin.lastIssue.%s%s' % (data.pil, data.pilExt)
        dsm.set(key, data.issueTime, 0, 0)
        ds.commit()
    
    if len(setlist):
        _signalRPC('playman.playCmd.bulletin.setList', (setlist,))
        twccommon.Log.info('set bulletins %s' % setlist)
    


def cancelBulletin(loc, pil, pilExt):
    b = twccommon.Data()
    b.pil = pil
    b.pilExt = pilExt
    b.group = ''
    cancelBulletin(loc, b)


def oldCancelBulletins(l):
    for loc, pil, pilExt in l:
        b = twccommon.Data()
        b.pil = pil
        b.pilExt = pilExt
        b.group = ''
        cancelBulletin(loc, b)
    


def cancelBulletin(loc, b):
    cancelBulletins([
        (loc, b)])


def cancelBulletins(l):
    setlist = []
    if len(l[0]) > 2:
        oldCancelBulletins(l)
    
    for loc, data in l:
        info = BulletinInfo.getBulletinProperties(data.pil, data.pilExt)
        groupOverride = getattr(info, 'groupOverride', 0)
        if groupOverride == 1 and data.group != '':
            group = data.group
        else:
            group = info.group
        which = '%s.%s' % (loc, group)
        key = 'bulletin.%s' % (which,)
        
        try:
            dsm.remove(key)
            ds.commit()
            setlist.append((loc, group))
        except KeyError:
            pass

    
    if len(setlist):
        _signalRPC('playman.playCmd.bulletin.cancelList', (setlist,))
        twccommon.Log.info('cancel bulletins %s' % setlist)
    


def setImageData(type, fname):
    twccommon.Log.info('setImageData(%s, %s)' % (type, fname))
    (imgType, imgLoc) = type.split('.')
    if imgType in [
        'map',
        'radar',
        'satellite',
        'radarSatellite']:
        fnName = 'execd.imageProc.%s.process' % imgType
    else:
        fnName = 'execd.imageProc.image.process'
    _signalRPC(fnName, (imgType, imgLoc, fname))
    twccommon.Log.info('set %s image: %s' % (type, fname))


def setMapCut(type):
    _signalRPC('execd.map.process', (type,))
    twccommon.Log.info('set map cut: %s' % type)


def setMapData(key, data, expiration, update = 0):
    mapForceKey = MAP_FORCE_KEY
    
    try:
        mapCutRequired = dsm.get(mapForceKey)
    except:
        mapCutRequired = 0

    mapDataKey = key + '.MapData'
    
    try:
        old = twc.DefaultedData(dsm.get(mapDataKey))
        for k, v1 in data.__dict__.items():
            v2 = getattr(old, k, None)
            if v2 != v1:
                mapCutRequired = 1
                break
            
    except:
        mapCutRequired = 1

    if mapCutRequired:
        pendingKey = MAP_PENDING_KEY
        
        try:
            mapPendingList = dsm.get(pendingKey)
        except KeyError:
            mapPendingList = []

        if mapPendingList.count(key) < 1:
            mapPendingList.append(key)
            dsm.set(pendingKey, mapPendingList, 0)
            ds.commit()
        
        twccommon.Log.info('set %s' % (mapDataKey,))
        _setData(mapDataKey, data, expiration, update)
        setMapCut(key)
    


def setInterestList(ilType, configVersion, val):
    if type(val) != types.ListType:
        raise RuntimeError, 'invalid interest list; should be a list of strings'
    
    key = 'Config.%s.interestlist.%s' % (configVersion, ilType)
    
    try:
        old = dsm.get(key)
    except KeyError:
        old = None

    if old != val:
        dsm.set(key, val, 0)
        ds.commit()
        twccommon.Log.info('setting %s to: %s' % (key, val))
        twc.InterestList.getInterestList(ilType, updateCache = 1)
        if _ilistSignalMap.has_key(ilType):
            for fnName in _ilistSignalMap[ilType]:
                _signalRPC(fnName, (val,))
            
        
    


def setTimeZone(timezone):
    twccommon.Log.info('setting timezone to: %s' % timezone)
    shutil.copyfile('/usr/share/zoneinfo/%s' % timezone, '/etc/localtime')


def installPackage(pkg, instPath):
    _signalRPC('execd.ipackage.install', (pkg, instPath))


def installMediaPack(pack, replace):
    _signalRPC('execd.mediapack.install', (pack, replace))


def getMediaPackVersion(pack):
    version = None
    versionFile = '/media/%s.version' % (pack,)
    if os.path.exists(versionFile):
        
        try:
            fd = open(versionFile, 'r')
            version = fd.readline()
            version = version[:-1]
            fd.close()
        except:
            twccommon.Log.warning('getMediaPackVersion: Error reading version file: %s.' % (versionFile,))

    else:
        twccommon.Log.info('getMediaPackVersion: Pack %s not installed.' % (pack,))
    return version


def shutdown():
    reboot()


def reboot():
    twccommon.Log.info('Shut down requested! Rebooting...')
    os.system('shutdown -r now')


def restart():
    twccommon.Log.info('Restart requested! Killing processes...')
    os.system('killall receiverd')


def loadClock():
    pass


def loadData(prodType, argData):
    if prodType == 'tag':
        id = 'tag-%s' % argData.id
        duration = argData.duration * 30 + argData.durationFrames
        scheds = "[DynamicSchedule('Tag')]"
        params = twccommon.Data(mediaNum = argData.mediaNum)
        _pmLoad(id, duration, argData.expire, scheds, params)
    elif prodType == 'localAvail':
        id = 'localAvail-%s' % argData.id
        duration = 68
        durationFrames = 0
        duration = duration * 30 + durationFrames
        scheds = "[DynamicSchedule('LocalAvail')]"
        params = twccommon.Data()
        _pmLoad(id, duration, argData.expire, scheds, params)
    elif prodType == 'SNUP':
        if len(argData.media1) > 0:
            displayMode = argData.media1
        else:
            displayMode = None
        _ldlIdList.append(argData.id)
        _runPlayCmd('ldl', 'load', argData.id, 1, displayMode)
    elif prodType == 'SNDN':
        pass
    elif prodType == 'local':
        _runPlayCmd(prodType, 'load', argData)
    


def runData(prodType, argData):
    if prodType == 'tag':
        id = 'tag-%s' % argData.id
        _pmRun(id, argData.time, argData.frame)
    elif prodType == 'localAvail':
        id = 'localAvail-%s' % argData.id
        _pmRun(id, argData.time, argData.frame)
    elif prodType == 'SNUP':
        _runPlayCmd('ldl', 'run', argData.id, argData.time, argData.frame)
    elif prodType == 'SNDN':
        if argData.id.upper() == 'LDL' or len(_ldlIdList) > 2:
            _removeAllLDLLayers()
        elif argData.id in _ldlIdList:
            _ldlIdList.remove(argData.id)
        
        _runPlayCmd('ldl', 'load', argData.id, 0, None)
    elif prodType == 'local':
        _runPlayCmd(prodType, 'run', argData)
    


def processHeartbeat(**kw):
    v = _getDictVal(kw, 'time')
    if v != None:
        (sec, millisec) = v
        _setTime(sec, millisec)
    
    dispMode = _getDictVal(kw, 'displayMode')
    if dispMode != '*':
        _processStateVal(kw, 'displayMode')
    
    _processStateVal(kw, 'sensorState')


def setTime(sec, millisec):
    pass


def setTrafficIncidents(path, compression = 'none'):
    twccommon.Log.info('Traffic: setTrafficIncidents: path %s, compression = "%s"' % (path, compression))
    _signalRPC('execd.traffic.processIncidents', (path, compression))


def setTrafficMap(path, hasData):
    if hasData:
        twccommon.Log.info('Traffic: setTrafficMap: path %s.' % path)
    else:
        twccommon.Log.info('Traffic: set Temp Unavail Traffic Map: path %s.' % path)


def changeIrdChannel(channelNumber):
    _signalRPC('execd.altFeed.channelChange', (channelNumber,))

DELAYED_CHANNEL_CHANGE = 0
IMMEDIATE_CHANNEL_CHANGE = 1

def setIrdChannel(channelNumber, switchMethod = DELAYED_CHANNEL_CHANGE):
    if switchMethod == IMMEDIATE_CHANNEL_CHANGE:
        twccommon.Log.info('AltFeed: IMMEDIATE ird channel change requested to channel %s.' % (channelNumber,))
        changeIrdChannel(channelNumber)
    else:
        _signalRPC('execd.altFeed.channelChangeRequest', (channelNumber,))
        twccommon.Log.info('AltFeed: ird channel change requested: Channel %s.' % (channelNumber,))


def system(cmd):
    _signalRPC('execd.system', (cmd,))


def toggleNationalLDL(activate, displayMode = None):
    _runPlayCmd('ldl', 'toggleNationalLDL', '0', activate, displayMode)

_ugcRegex = re.compile('[A-Z]{2}[ZC]([0-9]{3}[\\->])*[0-9]{3}')
_getInterestList = twc.InterestList.getInterestList
_ilistSignalMap = {
    'climId': [
        'playman.init.setClimIds'],
    'county': [
        'playman.playCmd.bulletin.setCountyInterestList'] }

def _addGroup(group):
    key = 'bulletin.groups'
    
    try:
        groups = dsm.get(key)
        groups = _delExpiredGroups(groups)
    except:
        groups = []

    if group not in groups:
        groups.append(group)
    
    dsm.set(key, groups, 0)


def _delExpiredGroups(groups):
    key = 'bulletin.groups'
    foundBull = 0
    listChanged = 0
    il = _getInterestList('county')
    for group in groups[:]:
        for county in il:
            
            try:
                dsm.get('bulletin.%s.%s' % (county, group))
                foundBull = 1
            except:
                pass

        
        if foundBull == 0:
            groups.remove(group)
            listChanged = 1
        
    
    if listChanged == 1:
        dsm.set(key, groups, 0)
    
    return groups


def _setData(key, data, expiration, update):
    dsm.set(key, data, expiration, update)
    ds.commit()


def _signalEvent(type, value):
    twc.MiscCorbaInterface.signalEvent(CHANNEL_NAME, type, value)


def _signalRPC(rpcName, args):
    twc.MiscCorbaInterface.signalEvent(CHANNEL_NAME, rpcName, repr(args))


def _parseUGCStateList(ugc):
    state = ugc[:3]
    ugc = ugc[3:]
    sp = ugc.split('-')
    locs = []
    for loc in sp:
        pos = loc.find('>')
        if pos == -1:
            locs.append('%s%03d' % (state, int(loc)))
        else:
            start = int(loc[:pos])
            end = int(loc[pos + 1:])
            for i in range(start, end + 1):
                locs.append('%s%03d' % (state, i))
            
    
    return locs


def _getDictVal(dict, key):
    val = None
    
    try:
        val = dict[key]
    except KeyError:
        pass

    return val


def _processStateVal(kw, valName):
    v = _getDictVal(kw, valName)
    if v == None:
        return None
    
    dsv = dsm.defaultedGet(valName, None)
    if v == dsv:
        return None
    
    _setData(valName, v, 0, 0)


def _pmLoad(id, duration, expire, scheds, params):
    args = (id, duration, expire, scheds, params)
    twccommon.Log.info('signalling load of %s (%s, %s, %s, %s)' % args)
    _signalRPC('playman.playCmd.pm.load', args)


def _pmRun(id, startTime, startFrame):
    args = (id, startTime, startFrame)
    twccommon.Log.info('signalling run of %s (%s, %s)' % args)
    _signalRPC('playman.playCmd.pm.run', args)


def _runPlayCmd(prodType, playCmd, *params):
    twccommon.Log.info('signalling %s of %s %s' % (playCmd, prodType, str(params)))
    fnName = 'playman.playCmd.%s.%s' % (prodType, playCmd)
    _signalRPC(fnName, params)


def _removeAllLDLLayers():
    global _ldlIdList
    for id in _ldlIdList:
        _runPlayCmd('ldl', 'load', id, 0, None)
    
    _ldlIdList = []

