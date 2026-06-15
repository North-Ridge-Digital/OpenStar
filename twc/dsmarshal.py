import new
import sys
import twc
import twc.DataStoreInterface as twc
import types
import twccommon
ds = twc.DataStoreInterface
_TYP_INT = 'int'
_TYP_FLT = 'float'
_TYP_STR = 'str'
_TYP_TUPLE = 'tuple'
_TYP_LIST = 'list'
_TYP_INST = 'struct'
_defaultDict = { }

def setDefault(key, data):
    _defaultDict[key] = data


def set(key, data, expiration, update = 0):
    if type(data) == types.StringType:
        ds.set([
            (key, data, expiration)])
        return ''
    
    if update:
        
        try:
            oldData = get(key)
        except KeyError:
            update = 0

    
    userData = None
    if update:
        t1 = type(data)
        t2 = type(oldData)
        if t1 != types.InstanceType or t2 != types.InstanceType:
            raise RuntimeError, 'cannot update non-instance type'
        
        userData = twc.Data()
        userData.__dict__.update(data.__dict__)
        temp = twc.Data()
        temp.__dict__.update(oldData.__dict__)
        temp.__dict__.update(data.__dict__)
        data = temp
    
    (formatStr, marshaledEntries) = _set(key, data, expiration, marshalStr = 1)
    if update:
        (tmp, marshaledEntries) = _set(key, userData, expiration, marshalStr = 1)
        marshaledEntries.append(('%s._dsmarshal' % key, formatStr, expiration))
    
    ds.set(marshaledEntries)
    return formatStr


def defaultedGet(key, default = None, cachingEnabled = None):
    '''Get the object referenced by key, else, return default obj if u cant 
find it'''
    
    try:
        return get(key, cachingEnabled)
    except KeyError:
        return default



def get(key, cachingEnabled = None):
    
    try:
        defaultResult = _defaultDict[key]
        if isinstance(defaultResult, twccommon.Data):
            defaultResult = defaultResult.clone()
    except KeyError:
        defaultResult = None

    
    try:
        formatKey = '%s._dsmarshal' % key
        (rc, data) = ds.get([
            key,
            formatKey], cachingEnabled)
        
        try:
            tokens = data[formatKey].split(' ')
        except KeyError:
            return data[key]

        fields = []
        maker = _parse(key, tokens, fields)
        if fields:
            (rc, data) = ds.get(fields, cachingEnabled)
        
        result = _make(maker, data)
        if isinstance(result, twccommon.Data) and isinstance(defaultResult, twccommon.Data):
            result = twccommon.mergeStructs([
                result], defaultResult)
        
        return result
    except KeyError:
        e = None
        if defaultResult != None:
            return defaultResult
        else:
            raise e
    except:
        defaultResult != None



def multiGet(keys, cachingEnabled = None):
    keyDict = { }
    dsKeys = []
    for key in keys:
        formatKey = '%s._dsmarshal' % key
        dsKeys.append(key)
        dsKeys.append(formatKey)
        d = twc.Data()
        d.formatKey = formatKey
        d.result = None
        d.maker = None
        keyDict[key] = d
    
    (rc, data) = ds.get(dsKeys, cachingEnabled)
    fields = []
    for key in keys:
        d = keyDict[key]
        
        try:
            tokens = data[d.formatKey].split(' ')
            d.maker = _parse(key, tokens, fields)
        except KeyError:
            
            try:
                d.result = data[key]
            except KeyError:
                d.result = None


    
    if fields:
        (rc, data) = ds.get(fields, cachingEnabled)
    
    result = []
    for key in keys:
        d = keyDict[key]
        if d.maker:
            result.append(_make(d.maker, data))
        else:
            result.append(d.result)
    
    return result


def configGet(key, cachingEnabled = None):
    '''Prepends a "Config.<configVersion>." to the incoming key,
       queries the datastore for the value of that key, and
       returns the value.

       The "configVersion" attribute is stored in the dataStore,
       and updated for each configuration release.  This allows
       us to decouple different config releases in the field.'''
    cfgKey = 'Config.' + str(get('configVersion')) + '.' + key
    return get(cfgKey, cachingEnabled)


def defaultedConfigGet(key, default = None, cachingEnabled = None):
    cfgKey = 'Config.' + str(get('configVersion')) + '.' + key
    
    try:
        return get(cfgKey, cachingEnabled)
    except KeyError:
        return default



def getConfigVersion():
    '''Returns the current configuration version.'''
    return str(get('configVersion'))


def remove(key):
    fields = []
    
    try:
        formatKey = '%s._dsmarshal' % key
        (rc, data) = ds.get([
            formatKey], cachingEnabled = 0)
        tokens = data[formatKey].split(' ')
        maker = _parse(key, tokens, fields)
        fields.append(formatKey)
    except KeyError:
        fields = [
            key]

    rc = ds.remove(fields)


def _set(key, data, expire, marshalStr = 0):
    t = type(data)
    if t is types.IntType:
        return _setAtomicType(key, _TYP_INT, data, expire, marshalStr)
    elif t is types.FloatType:
        return _setAtomicType(key, _TYP_FLT, data, expire, marshalStr)
    elif t is types.StringType:
        return _setAtomicType(key, _TYP_STR, data, expire, marshalStr)
    elif t is types.TupleType:
        fields = map((lambda a, b: (a, b)), range(len(data)), data)
        return _setContainerType(key, _TYP_TUPLE, '', fields, expire, marshalStr)
    elif t is types.ListType:
        fields = map((lambda a, b: (a, b)), range(len(data)), data)
        return _setContainerType(key, _TYP_LIST, '', fields, expire, marshalStr)
    elif t is types.InstanceType:
        cl = data.__class__
        args = '%s %s' % (cl.__module__, cl.__name__)
        return _setContainerType(key, _TYP_INST, args, data.__dict__.items(), expire, marshalStr)
    else:
        raise RuntimeError, '%s not supported by dsmarshal' % (str(t),)


def _setAtomicType(key, formatStr, data, expire, marshalStr):
    entries = []
    formatStr = '%s ' % formatStr
    if marshalStr:
        entries.append(('%s._dsmarshal' % key, formatStr, expire))
    
    entries.append((key, str(data), expire))
    return (formatStr, entries)


def _setContainerType(key, containerType, argsString, fields, expire, marshalStr):
    formatStr = ''
    entries = []
    for fieldName, val in fields:
        if val != None:
            (fs, ent) = _set('%s.%s' % (key, fieldName), val, expire)
            formatStr = formatStr + '%s %s' % (fieldName, fs)
            entries = entries + ent
        
    
    formatStr = '%s ( %s %s) ' % (containerType, argsString, formatStr)
    if marshalStr:
        entries.append(('%s._dsmarshal' % key, '%s' % formatStr, expire))
    
    return (formatStr, entries)


def _parse(field, tokens, fields):
    token = _getNextToken(tokens)
    if token == _TYP_INT:
        fields.append(field)
        return (field, _makeInt, ())
    elif token == _TYP_FLT:
        fields.append(field)
        return (field, _makeFlt, ())
    elif token == _TYP_STR:
        fields.append(field)
        return (field, _makeStr, ())
    elif token == _TYP_TUPLE:
        return _parseTuple(field, tokens, fields)
    elif token == _TYP_LIST:
        return _parseList(field, tokens, fields)
    elif token == _TYP_INST:
        return _parseInst(field, tokens, fields)
    else:
        raise RuntimeError, 'dsmarshal err: unexpected token %s' % token


def _parseTuple(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)
    return (field, _makeTuple, (makers,))


def _parseList(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)
    return (field, _makeList, (makers,))


def _parseInst(field, tokens, fields):
    _assume('(', _getNextToken(tokens))
    moduleName = _getNextToken(tokens)
    className = _getNextToken(tokens)
    makers = []
    token = _getNextToken(tokens)
    while token != ')':
        makers.append(_parse('%s.%s' % (field, token), tokens, fields))
        token = _getNextToken(tokens)
    return (field, _makeInst, (moduleName, className, makers))


def _getNextToken(tokens):
    token = ''
    while token == '':
        token = tokens[0]
        del tokens[0]
    return token


def _assume(expected, got):
    if expected != got:
        raise RuntimeError, 'dsmarshal err: expected "%s" got "%s"' % (expected, got)
    


def _make(maker, data):
    (field, makeFn, args) = maker
    args = (field, data) + args
    return apply(makeFn, args)


def _makeInt(field, data):
    
    try:
        return int(data[field])
    except KeyError:
        return None



def _makeFlt(field, data):
    
    try:
        return float(data[field])
    except KeyError:
        return None



def _makeStr(field, data):
    
    try:
        return data[field]
    except KeyError:
        return None



def _makeTuple(field, data, makers):
    res = ()
    for maker in makers:
        obj = _make(maker, data)
        res = res + (obj,)
    
    return res


def _makeList(field, data, makers):
    res = []
    for maker in makers:
        res.append(_make(maker, data))
    
    return res


def _makeInst(field, data, moduleName, className, makers):
    dict = { }
    for maker in makers:
        field = maker[0].split('.')[-1]
        dict[field] = _make(maker, data)
    
    mod = sys.modules[moduleName]
    cl = mod.__dict__[className]
    return new.instance(cl, dict)

