import os
import twccommon.embedded as twccommon
import twccommon.Log as twccommon
import _Configuration
import _twc

class Config:
    '''Le Config Base Class'''
    localConfDepth = 0
    
    def __init__(self):
        twccommon.embedded.setconfclass(self)

    
    def _finalize(self):
        pass

    
    def setPidFileDir(self, dir):
        _Configuration.setPidFileDir(dir)

    
    def setWorkDir(self, dir):
        '''Sets the work directory for the current process'''
        _Configuration.setWorkDir(dir)

    
    def getWorkDir(self):
        '''Returns the work directory for the current process'''
        return _Configuration.getWorkDir()

    
    def getSystemDataDir(self):
        '''Gets the system data directory'''
        return _Configuration.getSystemDataDir()

    
    def setLogLevel(self, level):
        '''Sets the current logging level'''
        _twc.setLogLevel(level)

    
    def setLogDir(self, dir):
        '''Sets directory to write application log'''
        _Configuration.setLogDir(dir)

    
    def setLogFlushAfterWrite(self, flushAfterWrite):
        '''Set to non zero to cause the log to be flushed to disk after every
        write.'''
        _Configuration.setLogFlushAfterWrite(flushAfterWrite)

    
    def setChannel(self, channel):
        '''Sets the name of the event channel to use (if appropriate)'''
        _Configuration.setChannel(channel)

    
    def setChannelFactory(self, factory):
        '''Sets the name of the event channel factory for creating new ones'''
        _Configuration.setChannelFactory(factory)

    
    def setAppName(self, name):
        '''Sets the name of the application (in case default isnt good enuf'''
        _Configuration.setAppName(name)
        twccommon.Log.setIdent(name)

    
    def doLocalConfig(self, filename):
        '''Runs local configuration.  Do NOT call this from a local conf file
        or else it will complain bitterly that you are stupid!'''
        Config.localConfDepth = Config.localConfDepth + 1
        if Config.localConfDepth > 1:
            raise RuntimeError, 'User Error: Do NOT call doLocalConfig ' + 'within a local conf file (FOOL!!!)!'
        
        localPath = os.environ['TWCROOT']
        localPath = localPath + '/local_conf/'
        script = localPath + filename
        if os.path.exists(script):
            execfile(script)
        
        Config.localConfDepth = Config.localConfDepth - 1


