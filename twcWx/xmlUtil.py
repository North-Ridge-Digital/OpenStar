import twccommon
import twccommon.Log as twccommon
import xml.sax as xml
OPTIONAL = 0
REQUIRED = 1

class LookupSAXHandler(twccommon.SAXHandler):
    
    def __init__(self, subHandlerClass):
        self.msghandler = subHandlerClass(self)

    
    def startRootNode(self, attrs):
        self.msghandler.begin()

    
    def endRootNode(self):
        self.msghandler.done()

    
    def dataDictionary(self):
        return self.msghandler.dataDictionary()



class LookupSubHandler(twccommon.SubHandler):
    
    def __init__(self, container):
        twccommon.SubHandler.__init__(self, container)
        self._dataDict = { }

    
    def _parseAttributes(self, attrs, elements):
        d = twccommon.Data()
        for tag, ctype, required in elements:
            
            try:
                value = attrs.getValueByQName(tag)
            except Exception:
                e = None
                value = None
                if required:
                    raise e
                
            except:
                required

            if value != None:
                value = ctype(value)
            
            setattr(d, tag, value)
        
        return d

    
    def dataDictionary(self):
        return self._dataDict



def parseXML(path, subHandlerClass):
    f = open(path)
    parser = xml.sax.make_parser()
    handler = LookupSAXHandler(subHandlerClass)
    parser.setContentHandler(handler)
    parser.parse(f)
    f.close()
    return handler.dataDictionary()

