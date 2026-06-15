'''
'''
import sys
import CosNaming
from omniORB import CORBA
from twccommon.corba import getNamePath
from twc.corba.ClientCore import DataStore
from twc.corba.ClientCore import DataStoreSession

class InterfaceImpl:
    
    def __init__(self):
        self._sessionManager = _SessionManager()
        self._cachingEnabled = 0
        self.clearCache()

    
    def get(self, keys, cachingEnabled = None):
        (rc, values, notfound) = self.internalGet(keys, cachingEnabled)
        return (rc, values)

    
    def getAll(self, keys, cachingEnabled = None):
        (rc, values, notfound) = self.internalGet(keys, cachingEnabled)
        values.update(notfound)
        return (rc, values)

    
    def internalGet(self, keys, cachingEnabled = None):
        '''Internal get implementation for get/getAll to use'''
        notfound = { }
        rc = 1
        if cachingEnabled == None:
            cachingEnabled = self._cachingEnabled
        
        cached = []
        uncached = []
        for key in keys:
            if self._cache.has_key(key):
                cached.append(key)
            else:
                uncached.append(key)
        
        numUncached = len(uncached)
        if numUncached > 0:
            (rc, values) = self._get(uncached)
            if not rc:
                return (0, { }, notfound)
            
        
        result = { }
        for key in cached:
            result[key] = self._cache[key]
        
        for i in range(numUncached):
            value = values[i]
            if value.valid:
                key = uncached[i]
                data = value.data
                result[key] = data
                if cachingEnabled:
                    self._cache[key] = data
                
            else:
                notfound[key] = None
        
        return (rc, result, notfound)

    
    def set(self, entries):
        rc = 1
        dsEntries = []
        for key, data, expir in entries:
            dsEntry = DataStoreSession.Entry(key, data, expir)
            dsEntries.append(dsEntry)
        
        
        try:
            session = self._sessionManager.getDataStoreSession()
            session.set(dsEntries)
            for key, data, expir in entries:
                self._invalid.append(key)
        except DataStoreSession.TransactionSizeExceeded:
            e = None
            rc = 0
            print 'max. transaction size exceeded; DataStore set failed'
        except CORBA.SystemException:
            e = None
            rc = 0
            self._sessionManager.resetSession()
            print 'CORBA.SystemException', e

        return rc

    
    def remove(self, keys):
        rc = 1
        
        try:
            session = self._sessionManager.getDataStoreSession()
            session.remove(keys)
            for key in keys:
                self._invalid.append(key)
        except DataStoreSession.TransactionSizeExceeded:
            e = None
            rc = 0
            print 'max. transaction size exceeded; DataStore remove failed'
        except CORBA.SystemException:
            e = None
            rc = 0
            self._sessionManager.resetSession()
            print 'CORBA.SystemException', e

        return rc

    
    def commit(self):
        rc = 1
        
        try:
            session = self._sessionManager.getDataStoreSession()
            session.commit()
            for key in self._invalid:
                if self._cache.has_key(key):
                    del self._cache[key]
                
            
            self._invalid = []
        except CORBA.SystemException:
            e = None
            rc = 0
            self._sessionManager.resetSession()
            print 'CORBA.SystemException', e

        return rc

    
    def abort(self):
        rc = 1
        
        try:
            session = self._sessionManager.getDataStoreSession()
            session.abort()
            self._invalid = []
        except CORBA.SystemException:
            e = None
            rc = 0
            self._sessionManager.resetSession()
            print 'CORBA.SystemException', e

        return rc

    
    def enableCaching(self, cachingEnabled = 1):
        self._cachingEnabled = cachingEnabled

    
    def clearCache(self):
        self._cache = { }
        self._invalid = []

    
    def _get(self, keys):
        '''Perform a straight DataStoreSession.get, i.e. ignore local cache.'''
        rc = 1
        result = []
        
        try:
            session = self._sessionManager.getDataStoreSession()
            result = session.get(keys)
        except CORBA.SystemException:
            e = None
            rc = 0
            self._sessionManager.resetSession()
            print 'CORBA.SystemException', e

        return (rc, result)



class _SessionManager:
    '''Simply calls DataStore.endSession() when the module is no longer used.'''
    
    def __init__(self):
        self.resetSession()
        self._orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
        self._ctx = self._orb.resolve_initial_references('NameService')
        self._ctx = self._ctx._narrow(CosNaming.NamingContext)
        self.path = getNamePath('DataStore')

    
    def __del__(self):
        if self.dataStoreSession != DataStoreSession._nil:
            self.endSession()
        

    
    def getDataStoreSession(self):
        if CORBA.is_nil(self.dataStoreSession):
            dataStore = self._ctx.resolve(self.path)
            self.dataStoreSession = dataStore.startSession()
        
        return self.dataStoreSession

    
    def endSession(self):
        dataStore = self._ctx.resolve(self.path)
        dataStore.endSession(self.dataStoreSession)

    
    def resetSession(self):
        self.dataStoreSession = DataStoreSession._nil


