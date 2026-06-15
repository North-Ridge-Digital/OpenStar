import twccommon
import twcWx.ClimoMapping as Climo
climo = Climo.ClimoMapping(0)

def getData(location, month, day, default = None):
    result = climo.get((month, day), location)
    if result == None:
        if default == None:
            result = twccommon.Data()
        else:
            result = default
    
    return result


def processDataFile(interestList):
    ''' Interface to store climatological data.
    '''
    for location in interestList:
        
        try:
            climo.load(location)
        except Exception:
            e = None
            twccommon.Log.error("ClimatologyDataManager couldn't load climatology data file %s: %s" % (location, e))

    

