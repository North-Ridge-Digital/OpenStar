import os
import os.path as os
import twc
import twc.MiscCorbaInterface as twc
import twc.dsmarshal as twc
import twc.psp as twc
import twccommon
import twccommon.PluginManager as twccommon
import types
import string
import domestic.BulletinInfo as domestic
import twcWx.dataUtil as wxDataUtil
from domestic.Heuristic import *
dsm = twc.dsmarshal
BulletinInfo = domestic.BulletinInfo

def tmpFile(dir, base = '', ext = 'tmp'):
    global _ID
    fname = '%s/%s_%d.%s' % (dir, base, _ID, ext)
    f = open(fname, 'w')
    _ID += 1
    return (fname, f)


def checkActiveWarnings():
    interestlist = dsm.defaultedConfigGet('interestlist.county', [])
    bulletins = BulletinInfo.loadActiveBulletins(interestlist)
    bKeys = bulletins.keys()
    for key in bKeys:
        if bulletins[key].category == BulletinInfo.CAT_WARNING:
            return 1
        
    
    return 0


def checkRadarPrecip(RadarProductName, location = 'us', imageList = None):
    """Checks for significant radar returns (precip) in a given image
       list. If a list isn't provided, it will look up the latest images
       on disk. If a list IS provided, then we ignore the ProductName and
       ConfigSet. This method assumes that the imageList passed in only
       contains valid images and is already sorted from OLDEST to NEWEST."""
    radarReturns = 0
    imageRoot = '/twc/data/volatile/images/radar/%s.cuts/' % location
    productString = 'Config.' + dsm.getConfigVersion() + '.' + RadarProductName
    if imageList == None:
        imageList = dataUtil.getValidFileList(dataPath = imageRoot, prefix = productString, suffix = '*[0-9].tif', startTimeNdx = 3, endTimeNdx = 4, sortIndex = 3)
    
    if len(imageList) == 0:
        twccommon.Log.warning('checkRadarPrecip: no valid images found for %s.' % (productString,))
        return radarReturns
    
    (issuetime, newestImageDataFileName) = imageList[len(imageList) - 1]
    (fname, ftype) = string.split(newestImageDataFileName, '.tif')
    statsFile = fname + '.data.index'
    twccommon.Log.info('checkRadarPrecip: examining radar index file %s' % (statsFile,))
    nsRain = { }
    if os.path.isfile(statsFile):
        execfile(statsFile, nsRain, nsRain)
    else:
        twccommon.Log.error('checkRadarPrecip: missing radar index file %s' % (statsFile,))
    if nsRain.has_key('loopRainDensity'):
        loopRainDensity = nsRain['loopRainDensity']
        twccommon.Log.info('checkRadarPrecip: %s loopRainDensity = %d' % (productString, loopRainDensity))
    else:
        loopRainDensity = 5
        msg = 'checkRadarPrecip: Error reading loopRainDensity from index file: %s. ' % (statsFile,)
        msg += 'Assuming loopRainDensity > 5 (echoes present).'
        twccommon.Log.warning(msg)
    if nsRain.has_key('maxPrecipType'):
        maxPrecipType = nsRain['maxPrecipType']
        twccommon.Log.info('checkRadarPrecip: %s maxPrecipType = %d' % (productString, maxPrecipType))
    else:
        maxPrecipType = 3
        msg = 'checkRadarPrecip: Error reading maxPrecipType from index file: %s. ' % (statsFile,)
        msg += 'Assuming maxPrecipType = 3 (winter colors present).'
        twccommon.Log.warning(msg)
    radarReturns = 1
    if loopRainDensity < 5:
        twccommon.Log.info('checkRadarPrecip: no rain, so radarReturns set to 0')
        radarReturns = 0
    else:
        twccommon.Log.info('checkRadarPrecip: rain echoes found (loopRainDensity > 5), radarReturns set to 1')
    winterColors = 1
    if maxPrecipType < 2:
        twccommon.Log.info("checkRadarPrecip: either 'no precip' or 'rain' detected")
        winterColors = 0
    else:
        twccommon.Log.info('checkRadarPrecip: mixed precip or snow detected')
    return (radarReturns, winterColors)


def checkCurrentConditionsPrecip(obsStations = None):
    hasPrecip = 0
    if obsStations == None:
        ob = dsm.defaultedConfigGet('Local_CurrentConditions')
        if ob == None:
            return hasPrecip
        
        obsStations = ob.obsStation
    
    obsList = []
    for stn in obsStations:
        obs = dsm.defaultedGet('obs.%s' % (stn,))
        if obs != None:
            obx = twccommon.DefaultedData(obs)
            obsList.append(obx.skyCondition)
        
    
    for skyCode in obsList:
        if skyCode != None:
            hasPrecip = wxDataUtil.skyConditionHasPrecip(skyCode)
        
    
    twccommon.Log.info('checkCurrentConditionsPrecip=%d' % (hasPrecip,))
    return hasPrecip


def checkTextForecastPrecip(coopId = None):
    hasPrecip = 0
    if coopId == None:
        fcst = dsm.defaultedConfigGet('Local_TextForecast')
        if fcst == None:
            return hasPrecip
        
        coopId = fcst.coopId
    
    twccommon.Log.info('NO PRECIP FOR YOU! (checkTextForecast=0)')
    return hasPrecip

_ID = 0
