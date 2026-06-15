import types
import twc
import twcWx.xmlUtil as xmlUtil
import twcWx.mapping as mapping

class SkyCondMappingHandler(xmlUtil.LookupSubHandler):
    
    def __init__(self, container):
        self._elements = [
            ('key', types.IntType, xmlUtil.REQUIRED),
            ('iconFile', types.StringType, xmlUtil.REQUIRED),
            ('textModifier', types.StringType, xmlUtil.REQUIRED),
            ('group', types.IntType, xmlUtil.OPTIONAL),
            ('precipitation', types.IntType, xmlUtil.OPTIONAL)]
        xmlUtil.LookupSubHandler.__init__(self, container)

    
    def startrecord(self, attrs):
        data = self._parseAttributes(attrs, self._elements)
        if data != None:
            key = data.key
            delattr(data, 'key')
            data = twc.DefaultedData(data)
            self._dataDict[key] = data
        


filePath = '/media/mappings/skyCondLocales/'

class SkyCondMapping(mapping.Map):
    
    def __init__(self, refresh = 0):
        mapping.Map.__init__(self, refresh)

    
    def _load(self, data):
        path = filePath + data + '.xml'
        map = xmlUtil.parseXML(path, SkyCondMappingHandler)
        if map:
            return (map, path)
        else:
            return None


