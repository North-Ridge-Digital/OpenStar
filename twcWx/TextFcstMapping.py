import types
import twcWx.xmlUtil as xmlUtil
import twcWx.mapping as mapping
import twc

class TextFcstMappingHandler(xmlUtil.LookupSubHandler):
    
    def __init__(self, container):
        self._elements = [
            ('key', types.StringType, xmlUtil.REQUIRED),
            ('text', types.StringType, xmlUtil.REQUIRED)]
        xmlUtil.LookupSubHandler.__init__(self, container)

    
    def startrecord(self, attrs):
        data = self._parseAttributes(attrs, self._elements)
        if data != None:
            key = data.key
            delattr(data, 'key')
            data = twc.DefaultedData(data)
            self._dataDict[key] = data
        


filePath = '/media/mappings/textForecast/'

class TextFcstMapping(mapping.Map):
    
    def __init__(self, refresh = 0):
        mapping.Map.__init__(self, refresh)

    
    def _load(self, data):
        path = filePath + data + '.xml'
        map = xmlUtil.parseXML(path, TextFcstMappingHandler)
        if map:
            return (map, path)
        else:
            return None


