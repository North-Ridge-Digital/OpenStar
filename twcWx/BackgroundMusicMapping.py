import types
import twc
import twcWx.xmlUtil as xmlUtil
import twcWx.mapping as mapping

class BackgroundMusicMappingHandler(xmlUtil.LookupSubHandler):
    
    def __init__(self, container):
        self._elements = [
            ('musicFile', types.StringType, xmlUtil.REQUIRED)]
        xmlUtil.LookupSubHandler.__init__(self, container)
        self._key = 0

    
    def startrecord(self, attrs):
        data = self._parseAttributes(attrs, self._elements)
        if data != None:
            key = self._key
            data = twc.DefaultedData(data)
            self._dataDict[key] = data
            self._key = self._key + 1
        


filePath = '/media/mappings/audio/'

class BackgroundMusicMapping(mapping.Map):
    
    def __init__(self, refresh = 0):
        mapping.Map.__init__(self, refresh)

    
    def getList(self, data):
        lmap = self._getMap(data)
        result = None
        if lmap is not None:
            keys = lmap.keys()
            keys.sort()
            result = map(lmap.get, keys)
        
        return result

    
    def _load(self, data):
        path = filePath + data + '.xml'
        
        try:
            map = xmlUtil.parseXML(path, BackgroundMusicMappingHandler)
            if map:
                return (map, path)
            else:
                return None
        except IOError:
            return None



