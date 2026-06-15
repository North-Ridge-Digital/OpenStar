import os.path as os
TRUE = 1
FALSE = 0

def _compare(a, b):
    return a == b


class Data:
    '''An empty data structure.  Useful for data structures with dynamic
    member fields, i.e. adding new member variables at run time.
    '''
    
    def __init__(self, other = None, **kw):
        self.update(other, **kw)

    
    def __repr__(self):
        c = self.__class__
        s = '%s.%s(' % (c.__module__, c.__name__)
        for k, v in self.__dict__.items():
            s += '%s=%s, ' % (k, repr(v))
        
        s += ')'
        return s

    
    def update(self, other = None, **kw):
        if other != None:
            self.__dict__.update(other.__dict__)
        
        self.__dict__.update(kw)

    
    def clone(self):
        other = Data()
        other.update(self)
        return other



class DefaultedData(Data):
    """An empty data structure, like Data.  This one, however, returns a 
    specified default value for any undefined field.  This avoid having 
    to set up alot of exception handlers in order to test whether a given 
    field is present.  It also accepts a Data in its c'tor.  This is useful 
    for wrapping an existing Data when the 'defualted' behavior is desired.
    
    example:
        d = Data(x=1, y=2)
        dd = DefaultedData(data=d, a=100)
        dd.x  =>  1
        dd.y  =>  2
        dd.a  =>  100
        dd.b  =>  None        
    """
    
    def __init__(self, data = Data(), default = None, **kw):
        data.__dict__.update(kw)
        self.__dict__['__default'] = default
        self.__dict__['__data'] = data

    
    def __getattr__(self, name):
        
        try:
            return self.__dict__['__data'].__dict__[name]
        except KeyError:
            if name[0:2] == '__' and name[-2:] == '__':
                raise AttributeError
            
            return self.__dict__['__default']


    
    def __setattr__(self, name, val):
        self.__dict__['__data'].__dict__[name] = val

    
    def __repr__(self):
        c = self.__class__
        sdata = repr(self.__dict__['__data'])
        s = '%s.%s(%s)' % (c.__module__, c.__name__, sdata)
        return s

    
    def __str__(self):
        return str(self.__dict__['__data'])



def mergeStructs(dataList, default = None):
    '''Take a list of Data() structures and merge into 1 structure
    containing the union of all fields of all structures.  In the 
    case of matching field names, the last item in the list takes 
    precedence.
    '''
    res = Data()
    if default != None:
        res.__dict__.update(default.__dict__)
    
    for data in dataList:
        res.__dict__.update(data.__dict__)
    
    return res


def compare(l, r):
    '''Compares 2 numbers in a way useful for the sort routine.'''
    if l < r:
        return -1
    elif l > r:
        return 1
    else:
        return 0


def findFirstFile(fname, dirList):
    """Find the 1st instance of the specified file name in the given directories.
    Search through the directories, in the list's order, for a file with the
    specified name.  The full path, including filename, of the first one found
    will be returned or None if one is not found.
    """
    for d in dirList:
        fullName = '%s/%s' % (d, fname)
        if os.path.exists(fullName):
            return fullName
        
    
    return None

import urllib
import xml.sax as xml
import os.path as os
import cStringIO
import string
import time
from string import find

class SAXHandler(xml.sax.handler.ContentHandler):
    '''Extend the start/end-Element methods of this class to use more tag-
    specific handlers provided in derived classes'''
    
    def startDocument(self):
        self._SAXHandler__tag = None

    
    def startElement(self, tag, attrs):
        self._SAXHandler__tag = tag
        handler = getattr(self, 'start%s' % (tag,), None)
        if handler != None:
            handler(attrs)
        

    
    def endElement(self, tag):
        handler = getattr(self, 'end%s' % (tag,), None)
        if handler != None:
            handler()
        
        self._SAXHandler__tag = None

    
    def characters(self, content):
        handler = getattr(self, 'characters%s' % self._SAXHandler__tag, None)
        if handler != None:
            handler(content)
        

    
    def ignoreableWhitespace(self, content):
        handler = getattr(self, 'ignoreableWhitespace%s' % (self._SAXHandler__tag,), None)
        if handler != None:
            handler(content)
        

    
    def getCurrentTag(self):
        return self._SAXHandler__tag



class SubHandler:
    '''This class implements a framework that allows a container class to be
    extended at runtime with various specialized "plug-ins".
    Basically, what you do is subclass this thing with whatever specialized
    handling methods a particular xml doc type needs.
    On init, this class will extend its (passed-in) container class with a bunch
    of tag-handling plug-in methods whose names begin with \'start\' and \'end\'.
    When you call deatch(), it removes these doc-specific tag handlers.
    To avoid run-time name conflicts, make sure the container class does not
    already have methods that begin with \'start\' or \'end\' AND have the same 
    name as methods in your derived class!'''
    
    def __init__(self, container):
        """Look for subclassed methods that begin with 'start' or 'end'.
        Add them to the containter class"""
        self._container = container
        for key in dir(self):
            if find(key, 'start', 0, 5) >= 0 and find(key, 'end', 0, 3) >= 0 or find(key, 'characters', 0, 10) >= 0:
                if hasattr(container, key) != 0:
                    raise RuntimeError, 'Method Name Conflict: %s' % (key,)
                
                setattr(container, key, getattr(self, key))
            
        

    
    def finished(self):
        pass

    
    def detach(self):
        '''Delete all the methods that were added to the container class'''
        for key in dir(self):
            if find(key, 'start', 0, 5) >= 0 and find(key, 'end', 0, 3) >= 0 or find(key, 'characters', 0, 10) >= 0:
                delattr(self._container, key)
            
        


