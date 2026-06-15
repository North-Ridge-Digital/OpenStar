import twc.dsmarshal as dsm
from twc.Heuristic import *

def getSchedule(schedName, duration, prodLoader):
    playlist = DynamicPlaylist(schedName, duration, prodLoader)
    return playlist.getSchedule()


class Playlist:
    
    def __init__(self, prodLoader):
        self._pl = prodLoader
        self._prods = { }

    
    def _getExistingProduct(self, key):
        
        try:
            return self._prods[key]
        except Exception:
            e = None
            return None


    
    def _getProduct(self, prodType, prodName, prodInst):
        key = (prodType, prodName, prodInst)
        prod = self._getExistingProduct(key)
        if prod == None:
            
            try:
                prod = self._pl.loadProduct(prodType, prodName, prodInst)
                self._prods[key] = prod
            except Exception:
                e = None
                twccommon.Log.logCurrentException('error loading product %s.%s' % (prodType, prodName))
                prod = None

        
        return prod



class DynamicPlaylist(Playlist):
    
    def __init__(self, plistName, frameDuration, prodLoader):
        Playlist.__init__(self, prodLoader)
        twccommon.Log.info("processing DynamicPlaylist '%s'" % plistName)
        self._lastProdFrameAdj = int(frameDuration) % 30
        self._duration = int(frameDuration) / 30
        if self._lastProdFrameAdj > 14:
            self._duration += 1
            self._lastProdFrameAdj = -(30 - self._lastProdFrameAdj)
        
        if self._duration == 0:
            self._duration = 1
            self._lastProdFrameAdj = frameDuration - 30
        
        self._plistName = plistName
        self._data = None
        self._plist = None
        self._loadHeuristic = None
        self._overHeuristic = None
        self._underHeuristic = None
        self._readPlaylistFromDataStore('Playlist.%s' % (plistName,))
        prodLoader.startProdType(self._data.prodPrefix)

    
    def _readPlaylistFromDataStore(self, key):
        plistKey = 'Config.' + dsm.getConfigVersion() + '.' + key
        self._data = dsm.defaultedGet(plistKey)
        if self._data:
            self._plist = self._data.playlist
            
            try:
                self._loadHeuristic = globals()[self._data.loadHeuristic]()
            except Exception:
                twccommon.Log.warning("playlist '%s' error with loadHeuristic '%s'" % (plistKey, self._data.loadHeuristic))
                raise 

            
            try:
                self._overHeuristic = globals()[self._data.overHeuristic]()
            except Exception:
                twccommon.Log.warning("playlist '%s' error with overHeuristic '%s'" % (plistKey, self._data.overHeuristic))
                raise 

            
            try:
                self._underHeuristic = globals()[self._data.underHeuristic]()
            except Exception:
                twccommon.Log.warning("playlist '%s' error with underHeuristic '%s'" % (plistKey, self._data.underHeuristic))
                raise 

        else:
            raise Exception("playlist '%s' not found" % (plistKey,))

    
    def getSchedule(self, schedDict = None):
        updateLastProd = 0
        if schedDict == None:
            updateLastProd = 1
            schedDict = { }
        
        schedule = self._initSchedule()
        self._loadHeuristic.debug(schedule, 'schedule before load:')
        (curDuration, schedule, runlist) = self._loadHeuristic.load(schedule, self._duration, self)
        loop = 0
        while curDuration != self._duration:
            if curDuration > self._duration:
                (curDuration, schedule, runlist) = self._overHeuristic.reduce(curDuration, schedule, runlist, self._duration, self)
            else:
                (curDuration, schedule, runlist) = self._underHeuristic.grow(curDuration, schedule, runlist, self._duration, self)
            loop += 1
            if loop > 100:
                raise Exception('abandoning playlist - heuristic loop > 100')
            
        prods = self._convertRunlist(runlist)
        if schedDict.has_key(self._data.prodPrefix):
            schedDict[self._data.prodPrefix].extend(prods)
        else:
            schedDict[self._data.prodPrefix] = prods
        self._processChildPlaylists(runlist, schedDict)
        if updateLastProd:
            for key, pList in schedDict.items():
                lastProd = pList[-1]
                duration = lastProd.getDuration()
                lastProd.setDuration(duration + self._lastProdFrameAdj)
                pgDurations = lastProd.getPageDurations()
                if pgDurations:
                    pgDurations[-1] += self._lastProdFrameAdj
                    lastProd.setPageDurations(pgDurations)
                
            
        
        return schedDict

    
    def _initSchedule(self):
        schedule = []
        pos = 0
        convert = 0
        if self._data.units == 'percent':
            convert = 1
        
        for prodName, prodInst, opt, max, min, step, pri, exclusive, cPlysts in self._plist:
            prodNameParts = prodName.split('.')
            prodName = prodNameParts[0]
            pageNum = 0
            if len(prodNameParts) > 1:
                pageNum = int(prodNameParts[1])
            
            pos += 1
            if convert:
                opt = int(opt * self._duration / 100)
                max = int(max * self._duration / 100)
                min = int(min * self._duration / 100)
            
            entry = [
                pos,
                pri,
                prodName,
                prodInst,
                pageNum,
                None,
                0,
                0,
                opt,
                max,
                min,
                step,
                exclusive,
                cPlysts]
            schedule.append(entry)
        
        return schedule

    
    def _convertRunlist(self, runlist):
        prods = []
        self._loadHeuristic.sortDisplay(runlist)
        self._loadHeuristic.debug(runlist, 'final runlist before conversion:')
        curProd = None
        curProdNm = None
        curDur = []
        curTotDur = 0
        curLastPg = 0
        for pe in runlist:
            if curProd:
                if pe[PRODNM_POS] == curProdNm:
                    if pe[PRODPG_POS] == curLastPg + 1:
                        dur = pe[CUR_POS] * 30
                        curDur.append(dur)
                        curTotDur += dur
                        curLastPg += 1
                        continue
                    else:
                        raise Exception('invalid playlist paged product pages not sequential')
                else:
                    curProd.setPageDurations(curDur)
                    curProd.setDuration(curTotDur)
                    prods.append(curProd)
                    curProd = None
                    curProdNm = None
                    curDur = []
                    curTotDur = 0
                    curLastPg = 0
            
            if not pe[PRODPG_POS]:
                pe[PROD_POS].setDuration(pe[CUR_POS] * 30)
                prods.append(pe[PROD_POS])
            elif pe[PRODPG_POS] == 1:
                curProd = pe[PROD_POS]
                curProdNm = pe[PRODNM_POS]
                dur = pe[CUR_POS] * 30
                curDur = [
                    dur]
                curTotDur += dur
                curLastPg = 1
            else:
                raise Exception("invalid playlist paged product '%s'display pos=%d does not start with 1" % (pe[PRODNM_POS], pe[DISP_POS]))
        
        if curProd:
            curProd.setPageDurations(curDur)
            curProd.setDuration(curTotDur)
            prods.append(curProd)
        
        return prods

    
    def _processChildPlaylists(self, runlist, schedDict):
        
        try:
            i = 0
            for child in self._data.childPrefixes:
                nxtPlaylist = None
                nxtDuration = 0
                for pe in runlist:
                    if nxtPlaylist:
                        if pe[CPLISTS_POS][i] == nxtPlaylist:
                            nxtDuration += pe[CUR_POS]
                            continue
                        else:
                            nxtDuration = nxtDuration * 30
                            p = DynamicPlaylist('%s.%s' % (child, nxtPlaylist), nxtDuration, self._pl)
                            schedDict = p.getSchedule(schedDict)
                    
                    nxtPlaylist = pe[CPLISTS_POS][i]
                    nxtDuration = pe[CUR_POS]
                
                if nxtPlaylist:
                    nxtDuration = nxtDuration * 30
                    p = DynamicPlaylist('%s.%s' % (child, nxtPlaylist), nxtDuration, self._pl)
                    schedDict = p.getSchedule(schedDict)
                
                i += 1
        except Exception:
            e = None
            twccommon.Log.logCurrentException("error attempting '%s' child playlist" % child)
            raise Exception("error attempting '%s' child playlist" % (child,))

        return schedDict

    
    def getProduct(self, prodName, prodInst):
        return self._getProduct(self._data.prodPrefix, prodName, prodInst)


