import _twc
import twccommon.Log as twccommon

class InterfaceImpl:
    '''Log using embedded C++ intrinsics so that log calls from 
    C++ code and embedded python interpreter are processed the same.
    (Avoids having 2 sets of log level functions, etc.)
    '''
    
    def setIdent(self, ident):
        ''' HAHAHAHA! '''
        pass

    
    def setLevel(self, level):
        _twc.setLogLevel(level)

    
    def critical(self, msg):
        _twc.logItem(twccommon.Log.CRIT, msg)

    
    def error(self, msg):
        _twc.logItem(twccommon.Log.ERR, msg)

    
    def warning(self, msg):
        _twc.logItem(twccommon.Log.WARN, msg)

    
    def info(self, msg):
        _twc.logItem(twccommon.Log.INFO, msg)

    
    def debug(self, msg):
        _twc.logItem(twccommon.Log.DBG, msg)


