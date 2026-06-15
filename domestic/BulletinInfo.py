import exceptions
import time
import twc
import twc.psp as twc
import twc.dsmarshal as twc
import twccommon
import twccommon.Log as twccommon
import sys
dsm = twc.dsmarshal
Log = twccommon.Log
CAT_WARNING = 3
CAT_WATCH = 2
CAT_ADVISORY = 1
BLUE_BKG = 0
YELLOW_BKG = 1
ORANGE_BKG = 2
RED_BKG = 3

class InvalidBulletin(exceptions.Exception):
    
    def __init__(self, args = None):
        self.args = args



def getPILs():
    """Get a list of all known pil and pil exyentions.
    return:
        A list of 2-element tuples, each containg a pil and a pil extention.
        Ex. [('TOR', '001'), ...]
    """
    data = dsm.defaultedConfigGet('interestlist.pil')
    if data == None:
        data = []
    
    return data


def getBulletinProperties(pil, pilExt):
    '''Get the properties for the specified pil and pilExt.
    params:
        pil    - The pil.
        pilExt - The pil extention.
    return:
        A structure containing data about the pil/pilExt including
        headline, color, priority, group, etc.
    exceptions:
        KeyError if either the pil or the pilExt is unknown.
    '''
    data = dsm.defaultedConfigGet('pil.%s%s' % (pil, pilExt))
    if data == None:
        ver = dsm.getConfigVersion()
        raise KeyError, "Config.%s.pil '%s%s' not found" % (ver, pil, pilExt)
    
    return data


def validateBulletin(bulletin):
    
    try:
        getattr(bulletin, 'pil')
        getattr(bulletin, 'pilExt')
        getattr(bulletin, 'expiration')
        getattr(bulletin, 'text')
        getattr(bulletin, 'issueTime')
        getattr(bulletin, 'dispExpiration')
    except AttributeError:
        e = None
        raise InvalidBulletin, str(e)



def loadBulletin(primaryCounty, county, group):
    key = 'bulletin.%s.%s' % (county, group)
    bulletin = dsm.get(key)
    return loadValidateBulletin(bulletin, primaryCounty, county, group)


def loadValidateBulletin(bulletin, primaryCounty, county, group):
    validateBulletin(bulletin)
    bulletinInfo = getBulletinProperties(bulletin.pil, bulletin.pilExt)
    text = getattr(bulletinInfo, 'text', None)
    if text:
        ns = { }
        ns.update(sys.modules)
        ns['bulletin'] = bulletin
        bulletinInfo.text = twc.psp.evalPage(text, ns)
    
    bulletin.__dict__.update(bulletinInfo.__dict__)
    bulletin.county = county
    bulletin.primary = bulletin.county == primaryCounty
    groupOverride = getattr(bulletinInfo, 'groupOverride', 0)
    if groupOverride == 1 and group != '':
        bulletin.group = group
    
    maxDispTime = getattr(bulletin, 'maxDispTime', None)
    if maxDispTime != None:
        now = time.time()
        bulletin.dispExpiration = min(now + maxDispTime, bulletin.dispExpiration)
    
    if getattr(bulletin, 'crawlGroup', None) == None:
        bulletin.crawlGroup = None
    
    return bulletin


def loadActiveBulletins(interestlist):
    grps = { }
    for pil, pilExt in getPILs():
        grps[getBulletinProperties(pil, pilExt).group] = 1
    
    groups = grps.keys()
    
    try:
        groups += dsm.get('bulletin.groups')
    except:
        pass

    bullKeys = []
    for county in interestlist:
        for group in groups:
            bullKeys.append('bulletin.%s.%s' % (county, group))
        
    
    bulls = []
    
    try:
        bulls = dsm.multiGet(bullKeys)
    except:
        pass

    bulletins = { }
    for county in interestlist:
        for group in groups:
            
            try:
                bull = bulls[0]
                bulls = bulls[1:]
                if bull:
                    bulletins[(county, group)] = loadValidateBulletin(bull, interestlist[0], county, group)
            except InvalidBulletin:
                e = None
                Log.warning('invalid bulletin found for %s.%s: %s' % (county, group, e))

        
    
    return bulletins

