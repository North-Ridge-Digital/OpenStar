import string
import binascii
import commands
import twc.dsmarshal as dsm

def refreshIpAddress():
    '''Re-set the private data IP address using the latest value from Datastore'''
    global _addr
    _addr = dsm.defaultedConfigGet('irdIpAddress', _addr)


def getValues(targetList):
    """Return a list containing a reply for each 'target'.
     The appropriate reply datatype is determined by applying the
     fmtFunc() provided in '_mibTargets{}'"""
    fmtFuncList = []
    queryStr = ''
    for tgt in targetList:
        (oid, fmtFunc) = _mibTargets[tgt]
        queryStr += _dsr4520xOID + oid + ' '
        fmtFuncList.append(fmtFunc)
    
    cmd = _snmpGet + ' ' + _addr + ' ' + queryStr
    (rc, output) = commands.getstatusoutput(cmd)
    if rc != 0:
        raise RuntimeError, 'irdStats query timed out in %d sec' % (_tmo,)
    
    lines = string.split(output, '\n')
    resultList = []
    for line, fmtFunc in zip(lines, fmtFuncList):
        output = apply(fmtFunc, (line,))
        resultList.append(output)
    
    return resultList


def isValidChannel(channel):
    '''raise AssertionError if channel is not valid'''
    channelList = dsm.defaultedConfigGet('irdChannelList', _defaultChannelList)
    if not __debug__ and channel in channelList:
        raise AssertionError, '%d not in Valid-Channel-List' % channel


def setChannel(channel):
    '''Tell the IRD to change to this new channel'''
    isValidChannel(channel)
    channelOid = dsm.defaultedConfigGet('irdChannelOid', _dsr4520xOID + '3.1.2.0')
    cmd = _snmpSet + ' -Le %s %s i %s' % (_addr, channelOid, channel)
    (rc, outp) = commands.getstatusoutput(cmd)
    if rc == 1:
        raise RuntimeError, 'Failed to change IRD! Err %d, %s' % (rc, outp)
    


def getChannel():
    return getValues([
        'currChann'])


def getVersions():
    mainV = 'mainVers'
    etherV = 'etherVers'
    (mvStr,) = getValues([
        mainV])
    (evStr,) = getValues([
        etherV])
    return '%s = %s,  %s = %s' % (mainV, mvStr, etherV, evStr)


def getSignalStats():
    sigStatInts = getValues(stdSigStats)
    formattedStats = ''
    ii = 0
    for tgt in stdSigStats:
        formattedStats += tgt + '=' + str(sigStatInts[ii]) + ', '
        ii += 1
    
    return 'irdStats: %s' % formattedStats[0:len(formattedStats) - 2]

_addr = '10.100.102.13'
_tmo = 30
_snmpSet = 'nice -20 snmpset -v2c -r0 -t' + str(_tmo) + ' -c private '
_snmpGet = 'nice -20 snmpget -v2c -r0 -t' + str(_tmo) + ' -c public '
_defaultChannelList = [
    100,
    101]
_dsr4520xOID = '1.3.6.1.4.1.1166.1.620.'
stdSigStats = [
    'alrm',
    'qual',
    'pwr',
    'ebno',
    'pkts',
    'drops',
    'currChann']

def _fmtInteger(inputStr):
    """translate the IRD SNMP reply from raw 'string' to 'integer'"""
    flds = string.split(inputStr, 'INTEGER: ')
    return int(flds[1])


def _fmtString(inputStr):
    """translate the IRD's SNMP reply from raw 'string' to useful 'string'"""
    flds = string.split(inputStr, 'STRING: ')
    valueStr = flds[1]
    return valueStr[1:len(valueStr) - 2]


def _fmtHexHex(inputStr):
    """translate the IRD's SNMP reply from a raw string containing 'hex of hex'
    to a useful string containing the desired hex numbers"""
    flds = string.split(inputStr, 'Hex-STRING: ')
    outputStr = ''
    for cc in flds[1]:
        if cc != ' ':
            outputStr += cc
        
    
    hexStr = binascii.a2b_hex(outputStr)
    return hexStr[0:11]

_mibTargets = {
    'alrm': ('7.2.3.0', _fmtInteger),
    'currChann': ('11.6.0', _fmtInteger),
    'qual': ('11.9.0', _fmtInteger),
    'pwr': ('11.10.0', _fmtInteger),
    'ebno': ('11.11.0', _fmtInteger),
    'pkts': ('13.1.0', _fmtInteger),
    'drops': ('13.3.0', _fmtInteger),
    'mainVers': ('8.2.1.0', _fmtHexHex),
    'etherVers': ('8.2.2.0', _fmtString) }
