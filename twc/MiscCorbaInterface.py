import twccommon.Log as twccommon
interface = None

def signalEvent(channelName, eventType, eventValue):
    return _getInterface().signalEvent(channelName, eventType, eventValue)


def runRenderScript(rsName, host = 'localhost', port = 4000, nsName = 'Renderd'):
    return _getInterface().runRenderScript(rsName, host, port, nsName)


def queueMovie(moviefile, host = 'localhost', port = 4000, nsName = 'Vspoold'):
    return _getInterface().queueMovie(moviefile, host, port, nsName)


def setMovieLooping(val, host = 'localhost', port = 4000, nsName = 'Vspoold'):
    return _getInterface().setMovieLooping(val, host, port, nsName)


def flushMovies(host = 'localhost', port = 4000, nsName = 'Vspoold'):
    return _getInterface().flushMovies(host, port, nsName)


def _getInterfaceInitial():
    global interface, _getInterface
    if interface == None:
        import twc.MiscCorbaInterfaceImpl as twc
        interface = twc.MiscCorbaInterfaceImpl.InterfaceImpl()
    
    _getInterface = _getInterfaceLoaded
    return interface


def _getInterfaceLoaded():
    return interface

_getInterface = _getInterfaceInitial
