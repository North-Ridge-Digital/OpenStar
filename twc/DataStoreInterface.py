'''Interface to the DataStore.  Access to the DataStore via
this interface encapsulates the CORBA IPC necessary to communicate
with the DataStore.  This interface also provides local caching
of DataStore values.  This avoids the IPC costs of retrieving the
same DataStore value multiple times.  This allows independent
modules to retrieve DataStore values independently (i.e. not having
to communicate which values have already been retrieved) with out
the extra IPC overhead.

This module also provides a extension mechanism that allows different
versions of the DataStore interface to be implemented w/o affecting
the callers of this module.  See DataStoreInterfaceImpl for more details.
'''
import twccommon
from twccommon import Data
interface = None

def init():
    '''Perform one time setup.
    '''
    global interface
    if interface == None:
        import twc.DataStoreInterfaceImpl as twc
        interface = twc.DataStoreInterfaceImpl.InterfaceImpl()
    


def uninit():
    '''Perform one time cleanup after this module is no longer 
    being used.
    '''
    global interface
    interface = None


def get(keys, cachingEnabled = None):
    '''Perform a get from the DataStore while honoring the local cache.
    Retrieves any keys whose values have been cached from the local
    cache.  Then any uncached values are retrieved from the DataStore.
    If caching is specified these values are then added to the local cache.

    Parameters:
    - keys: A list of key values to lookup in the DataStore.
    - cachingEnabled: Indicates wether the retrieved values should be
    put in the local cache.  If it has the value None (default)
    then the default caching-enabled flag is used.
    Note that previously cached values are pulled from the cache reguardless
    of this value.

    Return:
    Returns a 2 element tuple.  The first element is a boolean value
    indicating whether the operation was successfull.  The second
    is a dictionary containing the retrieved values keyed by their
    keys in the DataStore.
    '''
    return interface.get(keys, cachingEnabled)


def getAll(keys, cachingEnabled = None):
    return interface.getAll(keys, cachingEnabled)


def getData(keys, prefix = '', cachingEnabled = None):
    '''Rertieves data from the DataStore and returns it in a structure
    with fields to match each key in keys.  In other words, a structure
    is returned that contains one member variable, with a matching name,
    for each key requested.  If the key is not present in the DataStore,
    then the corresponding structure member variable will be set to None.
    (Remember all DataStore values are strings.)  If a prefix is supplied,
    then that string is appended to each key before looking it up in the 
    DataSore.  The prefix is not included in the structure member variable
    name, however.
    '''
    newKeys = []
    for key in keys:
        newKeys.append(prefix + key)
    
    (rc, ds) = get(newKeys, cachingEnabled)
    r = Data()
    for key in keys:
        
        try:
            r.__dict__[key] = ds[prefix + key]
        except KeyError:
            r.__dict__[key] = None

    
    return r


def set(entries):
    '''Set specified values in the DataStore while honoring the local cache.
    Any values set that have been previously cached, should me marked 
    for removal from the local cache upon a commit.  The cached values 
    should still be retrieved by subsequent calls to get() until commit() 
    is invoked.  If abort() is invoked the the cached values should then 
    be unmarked.

    Parameters:
    - entries: A list of 3 element tuples; each tuple contains a key, 
    a value, and a expiration time in time_t format.

    Return:
    Returns a boolean value indicating if the operation was successfull.
    '''
    return interface.set(entries)


def remove(keys):
    '''Remove values from the DataStore while honoring the local cache.
    Any values removed that have been previously cached, should me marked 
    for removal from the local cache upon a commit.  The cached values 
    should still be retrieved by subsequent calls to get() until commit() 
    is invoked.  If abort() is invoked the the cached values should then 
    be unmarked.

    Parameters:
    - keys: A list of key values to be removed from the DataStore.

    Return:
    Returns a boolean value indicating if the operation was successfull.
    '''
    return interface.remove(keys)


def commit():
    '''Commit outstanding changes on the DataStore and update local cache.
    Any values marked for removal from the local cache by either set()
    or remove() should now be remomved.  The intended effect of this is 
    to force any get() calls, for these values, to retrieve fresh values 
    from the DataStore.

    Parameters: none

    Return:
    Returns a boolean value indicating if the operation was successfull.
    '''
    return interface.commit()


def abort():
    '''Abort outstanding changes on the DataStore and update local cache.
    Any values marked for removal from the local cache by either set()
    or remove() should be unmarked.  The intendede effect of this is that 
    subsequent get() calls will continue to retrieve the cached values.
    Additionally, subsequent commit() calls will not affect these locally
    cached values (unless modified again by set() or remove()).

    Parameters: none

    Return:
    Returns a boolean value indicating if the operation was successfull.
    '''
    return interface.abort()


def enableCaching(cachingEnabled = 1):
    '''Set the default caching flag.
    This indicates whether get() calls should first attempt to 
    find previously cached values before retrieving values from 
    the DataStore.  Caching should be off by default (before any
    enableCaching() calls).  Invoking this function should not affect
    any already cached values.

    Parameters:
    - cachingEnabled: Boolean indicating new caching state.

    Return: none
    '''
    return interface.enableCaching(cachingEnabled)


def clearCache():
    '''Force the local cache to be cleared.
    Note that any markers set by set() or remove() should
    be removed as well.

    Parameters: none

    Return: none
    '''
    return interface.clearCache()

