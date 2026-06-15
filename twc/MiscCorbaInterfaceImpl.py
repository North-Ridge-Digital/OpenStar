import twccommon
from omniORB import CORBA
import twccommon.corba as twccommon
import twccommon.corba.CosEventComm__POA as twccommon
import twc.corba.ClientCore as twc
CHANNEL_IOR = 'corbaname::localhost:4000#%s'

class InterfaceImpl:
    
    def __init__(self):
        self._consumer = None
        self._renderd = None
        self._vspoold = None

    
    def signalEvent(self, chanName, eventType, eventValue):
        if self._consumer == None:
            channel = twccommon.corba.getOrb().string_to_object(CHANNEL_IOR % (chanName,))
            admin = channel.for_suppliers()
            self._consumer = admin.obtain_push_consumer()
        
        
        try:
            event = twc.corba.ClientCore.Event(eventType, eventValue)
            any = CORBA.Any(CORBA.TypeCode(twc.corba.ClientCore.Event), event)
            self._consumer.push(any)
        except:
            self._consumer = None
            raise 


    
    def runRenderScript(self, rsName, host, port, nsName):
        if self._renderd == None:
            self._renderd = twccommon.corba.getOrb().string_to_object('corbaname::%s:%d#%s' % (host, port, nsName))
        
        
        try:
            self._renderd.execPresentationScript(rsName)
        except:
            self._renderd = None
            raise 


    
    def queueMovie(self, moviefile, host, port, nsName):
        if self._vspoold == None:
            self._vspoold = twccommon.corba.getOrb().string_to_object('corbaname::%s:%d#%s' % (host, port, nsName))
        
        
        try:
            self._vspoold.addFile(moviefile + '.mpg')
        except:
            self._vspoold = None
            raise 


    
    def setMovieLooping(self, val, host, port, nsName):
        if self._vspoold == None:
            self._vspoold = twccommon.corba.getOrb().string_to_object('corbaname::%s:%d#%s' % (host, port, nsName))
        
        
        try:
            self._vspoold.setLooping(val)
        except:
            self._vspoold = None
            raise 


    
    def flushMovies(self, host, port, nsName):
        if self._vspoold == None:
            self._vspoold = twccommon.corba.getOrb().string_to_object('corbaname::%s:%d#%s' % (host, port, nsName))
        
        
        try:
            self._vspoold.flush()
        except:
            self._vspoold = None
            raise 



