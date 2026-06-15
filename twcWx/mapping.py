import os.path as os
import twccommon.Log as twccommon
_refresh = []

def refreshAll():
    for m in _refresh:
        m.refresh()
    


class Map:
    
    def __init__(self, refresh = 0):
        self._myMaps = { }
        if refresh:
            _refresh.append(self)
        

    
    def get(self, key, data):
        m = self._getMap(data)
        result = None
        if m:
            
            try:
                result = m[key]
            except KeyError:
                pass

        
        return result

    
    def _load(self, data):
        return None

    
    def load(self, data):
        lresult = self._load(data)
        if lresult:
            modTime = os.path.getmtime(lresult[1])
            self._myMaps[data] = (lresult[0], lresult[1], modTime)
            return lresult[0]
        else:
            twccommon.Log.error("Map couldn't load data file %s" % data)
            return None

    
    def refresh(self):
        for key in self._myMaps:
            
            try:
                (map, path, modTime) = self._myMaps[key]
                curModTime = os.path.getmtime(path)
                if curModTime != modTime:
                    self.load(key)
            except:
                twccommon.Log.error('Error refreshing data file %s' % path)
                twccommon.Log.logCurrentException()

        

    
    def _getMap(self, data):
        
        try:
            mdata = self._myMaps[data]
            return mdata[0]
        except KeyError:
            return self.load(data)



