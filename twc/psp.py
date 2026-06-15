import os.path as os
import string
import types
import twc.dsmarshal as twc
import twc.rsutil as rsutil
from twc import DataStoreInterface
_includePath = [
    '.']

def setIncludePath(path = []):
    global _includePath
    _includePath = path


def evalPage(page, namespace = { }, includePath = None):
    """Parses text looking for tags in the spirit of ASP tags and evaluates
    them.  The contexts of the tags are passed to the Python interpreter.
    The page, after evaluating the tags, is returned as the result of this 
    function.  Two type of tags are supported: '<%!...%>'  and '<%=...%>'.
    The contents of the '!' style tags are exec'd and the tag
    is removed from the original page.  The contents of the '=' style tags
    are eval'd and a string representation of the result is placed inline
    in the original text in place of the tag.  The provided namespace is 
    used by the Python interpreter.  Using the default parameter for this
    value causes a unique namespace to be created and used for each call.
    This implies that multiple tags w/in the same page (passed in text)
    share the namespace.  In other words one tag can create global values 
    that can be used by later tags.
    """
    if includePath == None:
        includePath = _includePath
    
    p1 = string.find(page, '<%')
    if p1 == -1:
        return page
    
    cmd = page[p1 + 2]
    p2 = string.find(page, '%>', p1)
    if p2 == -1:
        return page[:p1]
    
    sub1 = page[:p1]
    sub2 = page[p1 + 3:p2]
    sub3 = page[p2 + 2:]
    if cmd == '#':
        return sub1 + evalPage(sub3, namespace, includePath)
    elif cmd == '@':
        values = eval(sub2, namespace)
        if type(values) != types.ListType:
            values = [
                values]
        
        res = sub1
        for val in values:
            if val == None:
                continue
            
            val = str(val)
            fname = None
            if val[0] == '/':
                if os.path.exists(val):
                    fname = val
                
            else:
                for path in includePath:
                    temp = '%s/%s' % (path, val)
                    if os.path.exists(temp):
                        fname = temp
                        break
                    
                
            if fname == None:
                raise RuntimeError, 'file %s in PSP include tag not found' % sub2
            
            f = open(fname, 'r')
            sub2 = f.read()
            f.close()
            res += evalPage(sub2, namespace, includePath)
        
        res += evalPage(sub3, namespace, includePath)
        return res
    elif cmd == '!':
        exec sub2 in namespace
        return sub1 + evalPage(sub3, namespace, includePath)
    elif cmd == '=':
        return sub1 + str(eval(sub2, namespace)) + evalPage(sub3, namespace, includePath)
    elif cmd == '-':
        return sub1 + repr(eval(sub2, namespace)) + evalPage(sub3, namespace, includePath)
    else:
        raise RuntimeError, 'invalid psp tag %s' % (cmd,)


def evalRenderScript(page, namespace = { }, includePath = None):
    '''Same as eval but augments the namespace to include things
    that will be common to render script evaluation.  As an example,
    a get function will be added that retrieves data from the DataStore.
    '''
    namespace['rsutil'] = rsutil
    namespace['ds'] = DataStoreInterface
    namespace['dsm'] = twc.dsmarshal
    return evalPage(page, namespace, includePath)

