'''Defines the attributes of the various client processes.

This defines attributes that are needed at various places 
with client scripts.
'''
import os
import twc
import twccommon

class ClientAppInfo:
    '''Meta data used to run and monitor the various client processes.
    
    Note this class is simply a wrapper around related data.  There
    is, by intention, no encapsulation with get/set members since
    the data itself is the whole reason this class exists.
    '''
    
    def __init__(self, name, start, stop, blocking, sleep, monitored, script, core):
        self.name = name
        self.startOrder = start
        self.stopOrder = stop
        self.needsORBBlocking = blocking
        self.sleepAfterStart = sleep
        self.isMonitored = monitored
        self.isScript = script
        self.isCoreApp = core


_clientAppInfo = [
    ClientAppInfo('nsd', 0, 5, 0, 2, 0, 0, 0),
    ClientAppInfo('eventd', 1, 4, 0, 2, 0, 0, 0),
    ClientAppInfo('datad', 2, 3, 1, 0, 1, 0, 1),
    ClientAppInfo('receiverd', 3, 2, 1, 0, 1, 0, 1),
    ClientAppInfo('renderd', 4, 1, 1, 0, 1, 0, 1),
    ClientAppInfo('hc_monitor', 5, 0, 0, 0, 0, 1, 1)]

def getClientApps():
    '''Return list of client apps
    Returns a new copy of the list that can be sorted, etc.
    '''
    return filter(None, _clientAppInfo)


def getClientMonitoredApps():
    return filter((lambda client: client.isMonitored), getClientApps())


def getClientStartList():
    '''Returns a list of all client apps in the order they should be started.'''
    clients = getClientApps()
    clients.sort((lambda h1, h2: twccommon.compare(h1.startOrder, h2.startOrder)))
    return clients


def getClientStopList():
    '''Returns a list of all client apps in the order they should be started.'''
    clients = getClientApps()
    clients.sort((lambda h1, h2: twccommon.compare(h1.stopOrder, h2.stopOrder)))
    return clients


def getClientCoreStartList():
    '''Returns a list of CORE client apps in the order they should be started.'''
    clients = getClientStartList()
    return filter((lambda client: client.isCoreApp), clients)


def getClientNonCoreStartList():
    '''Returns a list of non-CORE client apps in the order they should be started.'''
    clients = getClientStartList()
    return filter((lambda client: client.isCoreApp == 0), clients)


def getClientCoreStopList():
    '''Returns a list of CORE client apps in the order they should be stopped.'''
    clients = getClientStopList()
    return filter((lambda client: client.isCoreApp), clients)


def getClientNonCoreStopList():
    '''Returns a list of non-CORE client apps in the order they should be stopped.'''
    clients = getClientStopList()
    return filter((lambda client: client.isCoreApp == 0), clients)

