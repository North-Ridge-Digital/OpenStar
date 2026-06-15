import os
import time
import types
import xml.sax.saxutils as saxutils

class IEvent:
    
    def typeName(self):
        pass

    
    def attributes(self):
        pass

    
    def content(self):
        pass



class Event(IEvent):
    
    def __init__(self, eventType = None, **kw):
        self.__dict__.update(kw)
        self._eventType = eventType

    
    def typeName(self):
        tn = getattr(self, '_eventType', None)
        if tn == None:
            return self.__class__.__name__
        else:
            return tn

    
    def attributes(self):
        attrs = self.__dict__.items()
        return filter((lambda e: e[0][0] != '_'), attrs)

    
    def content(self):
        return []



class EventLog:
    
    def __init__(self, basePath, rotationFreq):
        self.basePath = basePath
        self.workFile = '%s.tmp' % (basePath,)
        self.freq = rotationFreq
        now = int(time.time())
        self.nextRotation = self._calcNextRotationTime(now)

    
    def write(self, event):
        if not __debug__ and isinstance(event, IEvent):
            raise AssertionError
        self._rotate()
        self._write(event)

    
    def writeData(self, tag, data):
        self._rotate()
        self._writeData(tag, data)

    
    def _open(self):
        return file(self.workFile, 'a')

    
    def _write(self, event):
        s = _xmlifyEvent(event)
        f = self._open()
        f.write(s)
        f.close()

    
    def _writeData(self, tag, data):
        s = _xmlify(tag, data)
        f = self._open()
        f.write(s)
        f.close()

    
    def _rotate(self):
        now = int(time.time())
        if now > self.nextRotation:
            if os.path.exists(self.workFile):
                rfname = '%s_%s.log' % (self.basePath, self.nextRotation)
                os.rename(self.workFile, rfname)
            
            self.nextRotation = self._calcNextRotationTime(now)
        

    
    def _calcNextRotationTime(self, now):
        freq = self.freq
        return ((now + freq) / freq) * freq


INDENT_STR = '   '

def _sortChildrenByType(children):
    attrs = []
    content = []
    for k, v in children:
        if type(v) == types.InstanceType:
            content.append((k, v))
        else:
            attrs.append((k, v))
    
    return (attrs, content)


def _getChildren(data):
    if isinstance(data, IEvent):
        content = data.content()
        attrs = data.attributes()
        return (attrs, content)
    
    dtype = type(data)
    if dtype == types.InstanceType:
        return _sortChildrenByType(data.__dict__.items())
    elif dtype == types.DictionaryType:
        return _sortChildrenByType(data.items())
    
    return None


def _getDetailStrs(data, indent):
    children = _getChildren(data)
    cntStr = ''
    attrStr = ''
    if children == None:
        cntStr += str(data)
    else:
        (attrs, content) = children
        for k, v in content:
            cntStr += '\n' + _xmlifyData(k, v, indent + 1)
        
        if len(content) > 0:
            cntStr += '\n' + INDENT_STR * indent
        
        for k, v in attrs:
            attrStr += ' %s=%s' % (k, saxutils.quoteattr(str(v)))
        
    return (attrStr, cntStr)


def _xmlifyData(tag, data, indent):
    (attrStr, cntStr) = _getDetailStrs(data, indent)
    s = INDENT_STR * indent
    if len(cntStr) == 0:
        s += '<%s%s />' % (tag, attrStr)
    else:
        s += '<%s%s>%s</%s>' % (tag, attrStr, cntStr, tag)
    return s


def _xmlify(tag, data):
    return _xmlifyData(tag, data, 0) + '\n'


def _xmlifyEvent(event):
    eventType = event.typeName()
    attrStr = ''
    for k, v in event.attributes():
        attrStr += ' %s=%s' % (k, saxutils.quoteattr(str(v)))
    
    cntStr = ''
    for k, v in event.content():
        if isinstance(v, IEvent):
            cntStr += _xmlifyEvent(k, v)
        else:
            cntStr += '<%s>%s</%s>' % (k, saxutils.escape(str(v)), k)
    
    if len(cntStr) == 0:
        s = '<%s%s />\n' % (eventType, attrStr)
    else:
        s = '<%s%s>%s</%s>\n' % (eventType, attrStr, cntStr, eventType)
    return s

