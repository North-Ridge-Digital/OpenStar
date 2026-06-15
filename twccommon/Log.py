
import sys
import traceback
CRIT = 0
ERR = 1
WARN = 2
INFO = 3
DBG = 4
globalPfx = None
interface = None

def setIdent(ident):
    '''Set the identifing name that is printed w/ each log entry.'''
    _getInterface().setIdent(ident)


def setLevel(level):
    '''Set the logging level so that lower level messages are not logged.'''
    if level < CRIT or level > DBG:
        raise RuntimeError, 'invalid log level'
    
    _getInterface().setLevel(level)


def setPrefix(pfx):
    global globalPfx
    globalPfx = pfx


def clearPrefix():
    global globalPfx
    globalPfx = None


def tryPrefix(msg, pfx):
    '''Use the prefix-arg instead of the gloabal-prefix if one is passed in'''
    if pfx == None:
        pfx = globalPfx
    
    if pfx == None:
        return msg
    else:
        return '%s: %s' % (pfx, msg)


def critical(msg, pfx = None):
    _getInterface().critical(tryPrefix(msg, pfx))


def error(msg, pfx = None):
    _getInterface().error(tryPrefix(msg, pfx))


def warning(msg, pfx = None):
    _getInterface().warning(tryPrefix(msg, pfx))


def info(msg, pfx = None):
    _getInterface().info(tryPrefix(msg, pfx))


def debug(msg, pfx = None):
    _getInterface().debug(tryPrefix(msg, pfx))


def logCurrentException(prefix = ''):
    
    try:
        (etype, val, tb) = sys.exc_info()
        msg = traceback.format_exception(etype, val, tb)
        if prefix:
            msg = [
                prefix] + msg
        
        for mstr in msg:
            _getInterface().error(mstr)
    finally:
        etype = val = tb = None



def _getInterfaceInitial():
    global interface, _getInterface
    if interface == None:
        import twccommon.LogInterfaceImpl as twccommon
        interface = twccommon.LogInterfaceImpl.InterfaceImpl()
    
    interface.setLevel(INFO)
    _getInterface = _getInterfaceLoaded
    return interface


def _getInterfaceLoaded():
    return interface

_getInterface = _getInterfaceInitial
