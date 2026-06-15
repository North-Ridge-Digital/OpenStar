import omniORB
import _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(0, 5, __file__)
__name__ = 'twccommon.corba.TWCCore'
_0_TWCCore = omniORB.openModule('twccommon.corba.TWCCore', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/MonitorTarget.idl')
_0_TWCCore__POA = omniORB.openModule('twccommon.corba.TWCCore__POA', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/MonitorTarget.idl')

class StringList:
    _NP_RepositoryId = 'IDL:TWCCore/StringList:1.0'
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')


_0_TWCCore.StringList = StringList
_0_TWCCore._d_StringList = (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string, 0), 0)
_0_TWCCore._ad_StringList = (omniORB.tcInternal.tv_alias, StringList._NP_RepositoryId, 'StringList', (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string, 0), 0))
_0_TWCCore._tc_StringList = omniORB.tcInternal.createTypeCode(_0_TWCCore._ad_StringList)
omniORB.registerType(StringList._NP_RepositoryId, _0_TWCCore._ad_StringList, _0_TWCCore._tc_StringList)
del StringList
_0_TWCCore.UnknownNames = omniORB.newEmptyClass()

class UnknownNames(CORBA.UserException):
    _NP_RepositoryId = 'IDL:TWCCore/UnknownNames:1.0'
    
    def __init__(self, names):
        CORBA.UserException.__init__(self, names)
        self.names = names


_0_TWCCore.UnknownNames = UnknownNames
_0_TWCCore._d_UnknownNames = (omniORB.tcInternal.tv_except, UnknownNames, UnknownNames._NP_RepositoryId, 'UnknownNames', 'names', _0_TWCCore._d_StringList)
_0_TWCCore._tc_UnknownNames = omniORB.tcInternal.createTypeCode(_0_TWCCore._d_UnknownNames)
omniORB.registerType(UnknownNames._NP_RepositoryId, _0_TWCCore._d_UnknownNames, _0_TWCCore._tc_UnknownNames)
del UnknownNames
_0_TWCCore._d_MonitorTarget = (omniORB.tcInternal.tv_objref, 'IDL:TWCCore/MonitorTarget:1.0', 'MonitorTarget')
_0_TWCCore.MonitorTarget = omniORB.newEmptyClass()

class MonitorTarget:
    _NP_RepositoryId = _0_TWCCore._d_MonitorTarget[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_TWCCore.MonitorTarget = MonitorTarget
_0_TWCCore._tc_MonitorTarget = omniORB.tcInternal.createTypeCode(_0_TWCCore._d_MonitorTarget)
omniORB.registerType(MonitorTarget._NP_RepositoryId, _0_TWCCore._d_MonitorTarget, _0_TWCCore._tc_MonitorTarget)
MonitorTarget._d_getValues = ((_0_TWCCore._d_StringList,), (_0_TWCCore._d_StringList,), {
    _0_TWCCore.UnknownNames._NP_RepositoryId: _0_TWCCore._d_UnknownNames })
MonitorTarget._d_ping = ((), ((omniORB.tcInternal.tv_string, 0),), None)
MonitorTarget._d_getUptime = ((), (omniORB.tcInternal.tv_long,), None)
MonitorTarget._d_dbgcode = (((omniORB.tcInternal.tv_string, 0),), (), None)

class _objref_MonitorTarget(CORBA.Object):
    _NP_RepositoryId = MonitorTarget._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def getValues(self, *args):
        return _omnipy.invoke(self, 'getValues', _0_TWCCore.MonitorTarget._d_getValues, args)

    
    def ping(self, *args):
        return _omnipy.invoke(self, 'ping', _0_TWCCore.MonitorTarget._d_ping, args)

    
    def getUptime(self, *args):
        return _omnipy.invoke(self, 'getUptime', _0_TWCCore.MonitorTarget._d_getUptime, args)

    
    def dbgcode(self, *args):
        return _omnipy.invoke(self, 'dbgcode', _0_TWCCore.MonitorTarget._d_dbgcode, args)

    __methods__ = [
        'getValues',
        'ping',
        'getUptime',
        'dbgcode'] + CORBA.Object.__methods__

omniORB.registerObjref(MonitorTarget._NP_RepositoryId, _objref_MonitorTarget)
_0_TWCCore._objref_MonitorTarget = _objref_MonitorTarget
del MonitorTarget
del _objref_MonitorTarget
__name__ = 'twccommon.corba.TWCCore__POA'

class MonitorTarget(PortableServer.Servant):
    _NP_RepositoryId = _0_TWCCore.MonitorTarget._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'getValues': _0_TWCCore.MonitorTarget._d_getValues,
        'ping': _0_TWCCore.MonitorTarget._d_ping,
        'getUptime': _0_TWCCore.MonitorTarget._d_getUptime,
        'dbgcode': _0_TWCCore.MonitorTarget._d_dbgcode }

MonitorTarget._omni_skeleton = MonitorTarget
_0_TWCCore__POA.MonitorTarget = MonitorTarget
del MonitorTarget
__name__ = 'twccommon.corba.TWCCore'
__name__ = 'twccommon.corba.twccommon.corba.TWCCore_idl'
_exported_modules = ('twccommon.corba.TWCCore',)
