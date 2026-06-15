import os
import types
import twc
import twcWx.xmlUtil as xmlUtil
import twcWx.mapping as mapping
import twccommon
import twccommon.Log as twccommon

class ClimoMappingHandler(xmlUtil.LookupSubHandler):
    
    def __init__(self, container):
        self._elements = [
            ('loc', types.StringType, xmlUtil.REQUIRED),
            ('year', types.IntType, xmlUtil.REQUIRED),
            ('month', types.IntType, xmlUtil.REQUIRED),
            ('day', types.IntType, xmlUtil.REQUIRED),
            ('avgHigh', types.StringType, xmlUtil.OPTIONAL),
            ('avgLow', types.StringType, xmlUtil.OPTIONAL),
            ('recHigh', types.StringType, xmlUtil.OPTIONAL),
            ('recHighYear', types.StringType, xmlUtil.OPTIONAL),
            ('recLow', types.StringType, xmlUtil.OPTIONAL),
            ('recLowYear', types.StringType, xmlUtil.OPTIONAL)]
        xmlUtil.LookupSubHandler.__init__(self, container)

    
    def startClimoRec(self, attrs):
        data = self._parseAttributes(attrs, self._elements)
        if data != None:
            key = (data.month, data.day)
            data = twc.DefaultedData(data)
            self._dataDict[key] = data
        


TWCPERSDIR = os.environ['TWCPERSDIR']
filePath = '/usr/twc/data/climatology/'

class ClimoMapping(mapping.Map):
    
    def __init__(self, refresh = 0):
        mapping.Map.__init__(self, refresh)

    
    def _load(self, data):
        path = filePath + data + '.xml'
        map = xmlUtil.parseXML(path, ClimoMappingHandler)
        if map:
            return (map, path)
        else:
            return None


