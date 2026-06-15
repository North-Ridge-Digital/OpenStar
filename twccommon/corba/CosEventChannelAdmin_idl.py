import omniORB
import _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA
_omnipy.checkVersion(0, 5, __file__)
__name__ = 'twccommon.corba.CosEventComm'
_0_CosEventComm = omniORB.openModule('twccommon.corba.CosEventComm', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventComm.idl')
_0_CosEventComm__POA = omniORB.openModule('twccommon.corba.CosEventComm__POA', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventComm.idl')
_0_CosEventComm.Disconnected = omniORB.newEmptyClass()

class Disconnected(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosEventComm/Disconnected:1.0'

_0_CosEventComm.Disconnected = Disconnected
_0_CosEventComm._d_Disconnected = (omniORB.tcInternal.tv_except, Disconnected, Disconnected._NP_RepositoryId, 'Disconnected')
_0_CosEventComm._tc_Disconnected = omniORB.tcInternal.createTypeCode(_0_CosEventComm._d_Disconnected)
omniORB.registerType(Disconnected._NP_RepositoryId, _0_CosEventComm._d_Disconnected, _0_CosEventComm._tc_Disconnected)
del Disconnected
_0_CosEventComm._d_PushConsumer = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventComm/PushConsumer:1.0', 'PushConsumer')
_0_CosEventComm.PushConsumer = omniORB.newEmptyClass()

class PushConsumer:
    _NP_RepositoryId = _0_CosEventComm._d_PushConsumer[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventComm.PushConsumer = PushConsumer
_0_CosEventComm._tc_PushConsumer = omniORB.tcInternal.createTypeCode(_0_CosEventComm._d_PushConsumer)
omniORB.registerType(PushConsumer._NP_RepositoryId, _0_CosEventComm._d_PushConsumer, _0_CosEventComm._tc_PushConsumer)
PushConsumer._d_push = ((omniORB.tcInternal.tv_any,), (), {
    _0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected })
PushConsumer._d_disconnect_push_consumer = ((), (), None)

class _objref_PushConsumer(CORBA.Object):
    _NP_RepositoryId = PushConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def push(self, *args):
        return _omnipy.invoke(self, 'push', _0_CosEventComm.PushConsumer._d_push, args)

    
    def disconnect_push_consumer(self, *args):
        return _omnipy.invoke(self, 'disconnect_push_consumer', _0_CosEventComm.PushConsumer._d_disconnect_push_consumer, args)

    __methods__ = [
        'push',
        'disconnect_push_consumer'] + CORBA.Object.__methods__

omniORB.registerObjref(PushConsumer._NP_RepositoryId, _objref_PushConsumer)
_0_CosEventComm._objref_PushConsumer = _objref_PushConsumer
del PushConsumer
del _objref_PushConsumer
__name__ = 'twccommon.corba.CosEventComm__POA'

class PushConsumer(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventComm.PushConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'push': _0_CosEventComm.PushConsumer._d_push,
        'disconnect_push_consumer': _0_CosEventComm.PushConsumer._d_disconnect_push_consumer }

PushConsumer._omni_skeleton = PushConsumer
_0_CosEventComm__POA.PushConsumer = PushConsumer
del PushConsumer
__name__ = 'twccommon.corba.CosEventComm'
_0_CosEventComm._d_PushSupplier = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventComm/PushSupplier:1.0', 'PushSupplier')
_0_CosEventComm.PushSupplier = omniORB.newEmptyClass()

class PushSupplier:
    _NP_RepositoryId = _0_CosEventComm._d_PushSupplier[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventComm.PushSupplier = PushSupplier
_0_CosEventComm._tc_PushSupplier = omniORB.tcInternal.createTypeCode(_0_CosEventComm._d_PushSupplier)
omniORB.registerType(PushSupplier._NP_RepositoryId, _0_CosEventComm._d_PushSupplier, _0_CosEventComm._tc_PushSupplier)
PushSupplier._d_disconnect_push_supplier = ((), (), None)

class _objref_PushSupplier(CORBA.Object):
    _NP_RepositoryId = PushSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def disconnect_push_supplier(self, *args):
        return _omnipy.invoke(self, 'disconnect_push_supplier', _0_CosEventComm.PushSupplier._d_disconnect_push_supplier, args)

    __methods__ = [
        'disconnect_push_supplier'] + CORBA.Object.__methods__

omniORB.registerObjref(PushSupplier._NP_RepositoryId, _objref_PushSupplier)
_0_CosEventComm._objref_PushSupplier = _objref_PushSupplier
del PushSupplier
del _objref_PushSupplier
__name__ = 'twccommon.corba.CosEventComm__POA'

class PushSupplier(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventComm.PushSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'disconnect_push_supplier': _0_CosEventComm.PushSupplier._d_disconnect_push_supplier }

PushSupplier._omni_skeleton = PushSupplier
_0_CosEventComm__POA.PushSupplier = PushSupplier
del PushSupplier
__name__ = 'twccommon.corba.CosEventComm'
_0_CosEventComm._d_PullSupplier = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventComm/PullSupplier:1.0', 'PullSupplier')
_0_CosEventComm.PullSupplier = omniORB.newEmptyClass()

class PullSupplier:
    _NP_RepositoryId = _0_CosEventComm._d_PullSupplier[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventComm.PullSupplier = PullSupplier
_0_CosEventComm._tc_PullSupplier = omniORB.tcInternal.createTypeCode(_0_CosEventComm._d_PullSupplier)
omniORB.registerType(PullSupplier._NP_RepositoryId, _0_CosEventComm._d_PullSupplier, _0_CosEventComm._tc_PullSupplier)
PullSupplier._d_pull = ((), (omniORB.tcInternal.tv_any,), {
    _0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected })
PullSupplier._d_try_pull = ((), (omniORB.tcInternal.tv_any, omniORB.tcInternal.tv_boolean), {
    _0_CosEventComm.Disconnected._NP_RepositoryId: _0_CosEventComm._d_Disconnected })
PullSupplier._d_disconnect_pull_supplier = ((), (), None)

class _objref_PullSupplier(CORBA.Object):
    _NP_RepositoryId = PullSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def pull(self, *args):
        return _omnipy.invoke(self, 'pull', _0_CosEventComm.PullSupplier._d_pull, args)

    
    def try_pull(self, *args):
        return _omnipy.invoke(self, 'try_pull', _0_CosEventComm.PullSupplier._d_try_pull, args)

    
    def disconnect_pull_supplier(self, *args):
        return _omnipy.invoke(self, 'disconnect_pull_supplier', _0_CosEventComm.PullSupplier._d_disconnect_pull_supplier, args)

    __methods__ = [
        'pull',
        'try_pull',
        'disconnect_pull_supplier'] + CORBA.Object.__methods__

omniORB.registerObjref(PullSupplier._NP_RepositoryId, _objref_PullSupplier)
_0_CosEventComm._objref_PullSupplier = _objref_PullSupplier
del PullSupplier
del _objref_PullSupplier
__name__ = 'twccommon.corba.CosEventComm__POA'

class PullSupplier(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventComm.PullSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'pull': _0_CosEventComm.PullSupplier._d_pull,
        'try_pull': _0_CosEventComm.PullSupplier._d_try_pull,
        'disconnect_pull_supplier': _0_CosEventComm.PullSupplier._d_disconnect_pull_supplier }

PullSupplier._omni_skeleton = PullSupplier
_0_CosEventComm__POA.PullSupplier = PullSupplier
del PullSupplier
__name__ = 'twccommon.corba.CosEventComm'
_0_CosEventComm._d_PullConsumer = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventComm/PullConsumer:1.0', 'PullConsumer')
_0_CosEventComm.PullConsumer = omniORB.newEmptyClass()

class PullConsumer:
    _NP_RepositoryId = _0_CosEventComm._d_PullConsumer[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventComm.PullConsumer = PullConsumer
_0_CosEventComm._tc_PullConsumer = omniORB.tcInternal.createTypeCode(_0_CosEventComm._d_PullConsumer)
omniORB.registerType(PullConsumer._NP_RepositoryId, _0_CosEventComm._d_PullConsumer, _0_CosEventComm._tc_PullConsumer)
PullConsumer._d_disconnect_pull_consumer = ((), (), None)

class _objref_PullConsumer(CORBA.Object):
    _NP_RepositoryId = PullConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def disconnect_pull_consumer(self, *args):
        return _omnipy.invoke(self, 'disconnect_pull_consumer', _0_CosEventComm.PullConsumer._d_disconnect_pull_consumer, args)

    __methods__ = [
        'disconnect_pull_consumer'] + CORBA.Object.__methods__

omniORB.registerObjref(PullConsumer._NP_RepositoryId, _objref_PullConsumer)
_0_CosEventComm._objref_PullConsumer = _objref_PullConsumer
del PullConsumer
del _objref_PullConsumer
__name__ = 'twccommon.corba.CosEventComm__POA'

class PullConsumer(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventComm.PullConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'disconnect_pull_consumer': _0_CosEventComm.PullConsumer._d_disconnect_pull_consumer }

PullConsumer._omni_skeleton = PullConsumer
_0_CosEventComm__POA.PullConsumer = PullConsumer
del PullConsumer
__name__ = 'twccommon.corba.CosEventComm'
__name__ = 'twccommon.corba.twccommon.corba.CosEventChannelAdmin_idl'
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin = omniORB.openModule('twccommon.corba.CosEventChannelAdmin', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventChannelAdmin.idl')
_0_CosEventChannelAdmin__POA = omniORB.openModule('twccommon.corba.CosEventChannelAdmin__POA', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventChannelAdmin.idl')
_0_CosEventChannelAdmin.AlreadyConnected = omniORB.newEmptyClass()

class AlreadyConnected(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosEventChannelAdmin/AlreadyConnected:1.0'

_0_CosEventChannelAdmin.AlreadyConnected = AlreadyConnected
_0_CosEventChannelAdmin._d_AlreadyConnected = (omniORB.tcInternal.tv_except, AlreadyConnected, AlreadyConnected._NP_RepositoryId, 'AlreadyConnected')
_0_CosEventChannelAdmin._tc_AlreadyConnected = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_AlreadyConnected)
omniORB.registerType(AlreadyConnected._NP_RepositoryId, _0_CosEventChannelAdmin._d_AlreadyConnected, _0_CosEventChannelAdmin._tc_AlreadyConnected)
del AlreadyConnected
_0_CosEventChannelAdmin.TypeError = omniORB.newEmptyClass()

class TypeError(CORBA.UserException):
    _NP_RepositoryId = 'IDL:omg.org/CosEventChannelAdmin/TypeError:1.0'

_0_CosEventChannelAdmin.TypeError = TypeError
_0_CosEventChannelAdmin._d_TypeError = (omniORB.tcInternal.tv_except, TypeError, TypeError._NP_RepositoryId, 'TypeError')
_0_CosEventChannelAdmin._tc_TypeError = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_TypeError)
omniORB.registerType(TypeError._NP_RepositoryId, _0_CosEventChannelAdmin._d_TypeError, _0_CosEventChannelAdmin._tc_TypeError)
del TypeError
_0_CosEventChannelAdmin._d_ProxyPushConsumer = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/ProxyPushConsumer:1.0', 'ProxyPushConsumer')
_0_CosEventChannelAdmin.ProxyPushConsumer = omniORB.newEmptyClass()

class ProxyPushConsumer(_0_CosEventComm.PushConsumer):
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_ProxyPushConsumer[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.ProxyPushConsumer = ProxyPushConsumer
_0_CosEventChannelAdmin._tc_ProxyPushConsumer = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_ProxyPushConsumer)
omniORB.registerType(ProxyPushConsumer._NP_RepositoryId, _0_CosEventChannelAdmin._d_ProxyPushConsumer, _0_CosEventChannelAdmin._tc_ProxyPushConsumer)
ProxyPushConsumer._d_connect_push_supplier = ((_0_CosEventComm._d_PushSupplier,), (), {
    _0_CosEventChannelAdmin.AlreadyConnected._NP_RepositoryId: _0_CosEventChannelAdmin._d_AlreadyConnected })

class _objref_ProxyPushConsumer(_0_CosEventComm._objref_PushConsumer):
    _NP_RepositoryId = ProxyPushConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def connect_push_supplier(self, *args):
        return _omnipy.invoke(self, 'connect_push_supplier', _0_CosEventChannelAdmin.ProxyPushConsumer._d_connect_push_supplier, args)

    __methods__ = [
        'connect_push_supplier'] + _0_CosEventComm._objref_PushConsumer.__methods__

omniORB.registerObjref(ProxyPushConsumer._NP_RepositoryId, _objref_ProxyPushConsumer)
_0_CosEventChannelAdmin._objref_ProxyPushConsumer = _objref_ProxyPushConsumer
del ProxyPushConsumer
del _objref_ProxyPushConsumer
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class ProxyPushConsumer(_0_CosEventComm__POA.PushConsumer):
    _NP_RepositoryId = _0_CosEventChannelAdmin.ProxyPushConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'connect_push_supplier': _0_CosEventChannelAdmin.ProxyPushConsumer._d_connect_push_supplier }
    _omni_op_d.update(_0_CosEventComm__POA.PushConsumer._omni_op_d)

ProxyPushConsumer._omni_skeleton = ProxyPushConsumer
_0_CosEventChannelAdmin__POA.ProxyPushConsumer = ProxyPushConsumer
del ProxyPushConsumer
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_ProxyPullSupplier = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/ProxyPullSupplier:1.0', 'ProxyPullSupplier')
_0_CosEventChannelAdmin.ProxyPullSupplier = omniORB.newEmptyClass()

class ProxyPullSupplier(_0_CosEventComm.PullSupplier):
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_ProxyPullSupplier[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.ProxyPullSupplier = ProxyPullSupplier
_0_CosEventChannelAdmin._tc_ProxyPullSupplier = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_ProxyPullSupplier)
omniORB.registerType(ProxyPullSupplier._NP_RepositoryId, _0_CosEventChannelAdmin._d_ProxyPullSupplier, _0_CosEventChannelAdmin._tc_ProxyPullSupplier)
ProxyPullSupplier._d_connect_pull_consumer = ((_0_CosEventComm._d_PullConsumer,), (), {
    _0_CosEventChannelAdmin.AlreadyConnected._NP_RepositoryId: _0_CosEventChannelAdmin._d_AlreadyConnected })
ProxyPullSupplier._d_notify = ((omniORB.tcInternal.tv_any,), (), None)

class _objref_ProxyPullSupplier(_0_CosEventComm._objref_PullSupplier):
    _NP_RepositoryId = ProxyPullSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def connect_pull_consumer(self, *args):
        return _omnipy.invoke(self, 'connect_pull_consumer', _0_CosEventChannelAdmin.ProxyPullSupplier._d_connect_pull_consumer, args)

    
    def notify(self, *args):
        return _omnipy.invoke(self, 'notify', _0_CosEventChannelAdmin.ProxyPullSupplier._d_notify, args)

    __methods__ = [
        'connect_pull_consumer',
        'notify'] + _0_CosEventComm._objref_PullSupplier.__methods__

omniORB.registerObjref(ProxyPullSupplier._NP_RepositoryId, _objref_ProxyPullSupplier)
_0_CosEventChannelAdmin._objref_ProxyPullSupplier = _objref_ProxyPullSupplier
del ProxyPullSupplier
del _objref_ProxyPullSupplier
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class ProxyPullSupplier(_0_CosEventComm__POA.PullSupplier):
    _NP_RepositoryId = _0_CosEventChannelAdmin.ProxyPullSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'connect_pull_consumer': _0_CosEventChannelAdmin.ProxyPullSupplier._d_connect_pull_consumer,
        'notify': _0_CosEventChannelAdmin.ProxyPullSupplier._d_notify }
    _omni_op_d.update(_0_CosEventComm__POA.PullSupplier._omni_op_d)

ProxyPullSupplier._omni_skeleton = ProxyPullSupplier
_0_CosEventChannelAdmin__POA.ProxyPullSupplier = ProxyPullSupplier
del ProxyPullSupplier
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_ProxyPullConsumer = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/ProxyPullConsumer:1.0', 'ProxyPullConsumer')
_0_CosEventChannelAdmin.ProxyPullConsumer = omniORB.newEmptyClass()

class ProxyPullConsumer(_0_CosEventComm.PullConsumer):
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_ProxyPullConsumer[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.ProxyPullConsumer = ProxyPullConsumer
_0_CosEventChannelAdmin._tc_ProxyPullConsumer = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_ProxyPullConsumer)
omniORB.registerType(ProxyPullConsumer._NP_RepositoryId, _0_CosEventChannelAdmin._d_ProxyPullConsumer, _0_CosEventChannelAdmin._tc_ProxyPullConsumer)
ProxyPullConsumer._d_connect_pull_supplier = ((_0_CosEventComm._d_PullSupplier,), (), {
    _0_CosEventChannelAdmin.AlreadyConnected._NP_RepositoryId: _0_CosEventChannelAdmin._d_AlreadyConnected,
    _0_CosEventChannelAdmin.TypeError._NP_RepositoryId: _0_CosEventChannelAdmin._d_TypeError })
ProxyPullConsumer._d_listen = ((), (), None)

class _objref_ProxyPullConsumer(_0_CosEventComm._objref_PullConsumer):
    _NP_RepositoryId = ProxyPullConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def connect_pull_supplier(self, *args):
        return _omnipy.invoke(self, 'connect_pull_supplier', _0_CosEventChannelAdmin.ProxyPullConsumer._d_connect_pull_supplier, args)

    
    def listen(self, *args):
        return _omnipy.invoke(self, 'listen', _0_CosEventChannelAdmin.ProxyPullConsumer._d_listen, args)

    __methods__ = [
        'connect_pull_supplier',
        'listen'] + _0_CosEventComm._objref_PullConsumer.__methods__

omniORB.registerObjref(ProxyPullConsumer._NP_RepositoryId, _objref_ProxyPullConsumer)
_0_CosEventChannelAdmin._objref_ProxyPullConsumer = _objref_ProxyPullConsumer
del ProxyPullConsumer
del _objref_ProxyPullConsumer
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class ProxyPullConsumer(_0_CosEventComm__POA.PullConsumer):
    _NP_RepositoryId = _0_CosEventChannelAdmin.ProxyPullConsumer._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'connect_pull_supplier': _0_CosEventChannelAdmin.ProxyPullConsumer._d_connect_pull_supplier,
        'listen': _0_CosEventChannelAdmin.ProxyPullConsumer._d_listen }
    _omni_op_d.update(_0_CosEventComm__POA.PullConsumer._omni_op_d)

ProxyPullConsumer._omni_skeleton = ProxyPullConsumer
_0_CosEventChannelAdmin__POA.ProxyPullConsumer = ProxyPullConsumer
del ProxyPullConsumer
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_ProxyPushSupplier = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/ProxyPushSupplier:1.0', 'ProxyPushSupplier')
_0_CosEventChannelAdmin.ProxyPushSupplier = omniORB.newEmptyClass()

class ProxyPushSupplier(_0_CosEventComm.PushSupplier):
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_ProxyPushSupplier[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.ProxyPushSupplier = ProxyPushSupplier
_0_CosEventChannelAdmin._tc_ProxyPushSupplier = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_ProxyPushSupplier)
omniORB.registerType(ProxyPushSupplier._NP_RepositoryId, _0_CosEventChannelAdmin._d_ProxyPushSupplier, _0_CosEventChannelAdmin._tc_ProxyPushSupplier)
ProxyPushSupplier._d_connect_push_consumer = ((_0_CosEventComm._d_PushConsumer,), (), {
    _0_CosEventChannelAdmin.AlreadyConnected._NP_RepositoryId: _0_CosEventChannelAdmin._d_AlreadyConnected,
    _0_CosEventChannelAdmin.TypeError._NP_RepositoryId: _0_CosEventChannelAdmin._d_TypeError })
ProxyPushSupplier._d_notify = ((omniORB.tcInternal.tv_any,), (), None)

class _objref_ProxyPushSupplier(_0_CosEventComm._objref_PushSupplier):
    _NP_RepositoryId = ProxyPushSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def connect_push_consumer(self, *args):
        return _omnipy.invoke(self, 'connect_push_consumer', _0_CosEventChannelAdmin.ProxyPushSupplier._d_connect_push_consumer, args)

    
    def notify(self, *args):
        return _omnipy.invoke(self, 'notify', _0_CosEventChannelAdmin.ProxyPushSupplier._d_notify, args)

    __methods__ = [
        'connect_push_consumer',
        'notify'] + _0_CosEventComm._objref_PushSupplier.__methods__

omniORB.registerObjref(ProxyPushSupplier._NP_RepositoryId, _objref_ProxyPushSupplier)
_0_CosEventChannelAdmin._objref_ProxyPushSupplier = _objref_ProxyPushSupplier
del ProxyPushSupplier
del _objref_ProxyPushSupplier
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class ProxyPushSupplier(_0_CosEventComm__POA.PushSupplier):
    _NP_RepositoryId = _0_CosEventChannelAdmin.ProxyPushSupplier._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'connect_push_consumer': _0_CosEventChannelAdmin.ProxyPushSupplier._d_connect_push_consumer,
        'notify': _0_CosEventChannelAdmin.ProxyPushSupplier._d_notify }
    _omni_op_d.update(_0_CosEventComm__POA.PushSupplier._omni_op_d)

ProxyPushSupplier._omni_skeleton = ProxyPushSupplier
_0_CosEventChannelAdmin__POA.ProxyPushSupplier = ProxyPushSupplier
del ProxyPushSupplier
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_ConsumerAdmin = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/ConsumerAdmin:1.0', 'ConsumerAdmin')
_0_CosEventChannelAdmin.ConsumerAdmin = omniORB.newEmptyClass()

class ConsumerAdmin:
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_ConsumerAdmin[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.ConsumerAdmin = ConsumerAdmin
_0_CosEventChannelAdmin._tc_ConsumerAdmin = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_ConsumerAdmin)
omniORB.registerType(ConsumerAdmin._NP_RepositoryId, _0_CosEventChannelAdmin._d_ConsumerAdmin, _0_CosEventChannelAdmin._tc_ConsumerAdmin)
ConsumerAdmin._d_obtain_push_supplier = ((), (_0_CosEventChannelAdmin._d_ProxyPushSupplier,), None)
ConsumerAdmin._d_obtain_pull_supplier = ((), (_0_CosEventChannelAdmin._d_ProxyPullSupplier,), None)

class _objref_ConsumerAdmin(CORBA.Object):
    _NP_RepositoryId = ConsumerAdmin._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def obtain_push_supplier(self, *args):
        return _omnipy.invoke(self, 'obtain_push_supplier', _0_CosEventChannelAdmin.ConsumerAdmin._d_obtain_push_supplier, args)

    
    def obtain_pull_supplier(self, *args):
        return _omnipy.invoke(self, 'obtain_pull_supplier', _0_CosEventChannelAdmin.ConsumerAdmin._d_obtain_pull_supplier, args)

    __methods__ = [
        'obtain_push_supplier',
        'obtain_pull_supplier'] + CORBA.Object.__methods__

omniORB.registerObjref(ConsumerAdmin._NP_RepositoryId, _objref_ConsumerAdmin)
_0_CosEventChannelAdmin._objref_ConsumerAdmin = _objref_ConsumerAdmin
del ConsumerAdmin
del _objref_ConsumerAdmin
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class ConsumerAdmin(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventChannelAdmin.ConsumerAdmin._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'obtain_push_supplier': _0_CosEventChannelAdmin.ConsumerAdmin._d_obtain_push_supplier,
        'obtain_pull_supplier': _0_CosEventChannelAdmin.ConsumerAdmin._d_obtain_pull_supplier }

ConsumerAdmin._omni_skeleton = ConsumerAdmin
_0_CosEventChannelAdmin__POA.ConsumerAdmin = ConsumerAdmin
del ConsumerAdmin
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_SupplierAdmin = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/SupplierAdmin:1.0', 'SupplierAdmin')
_0_CosEventChannelAdmin.SupplierAdmin = omniORB.newEmptyClass()

class SupplierAdmin:
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_SupplierAdmin[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.SupplierAdmin = SupplierAdmin
_0_CosEventChannelAdmin._tc_SupplierAdmin = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_SupplierAdmin)
omniORB.registerType(SupplierAdmin._NP_RepositoryId, _0_CosEventChannelAdmin._d_SupplierAdmin, _0_CosEventChannelAdmin._tc_SupplierAdmin)
SupplierAdmin._d_obtain_push_consumer = ((), (_0_CosEventChannelAdmin._d_ProxyPushConsumer,), None)
SupplierAdmin._d_obtain_pull_consumer = ((), (_0_CosEventChannelAdmin._d_ProxyPullConsumer,), None)

class _objref_SupplierAdmin(CORBA.Object):
    _NP_RepositoryId = SupplierAdmin._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def obtain_push_consumer(self, *args):
        return _omnipy.invoke(self, 'obtain_push_consumer', _0_CosEventChannelAdmin.SupplierAdmin._d_obtain_push_consumer, args)

    
    def obtain_pull_consumer(self, *args):
        return _omnipy.invoke(self, 'obtain_pull_consumer', _0_CosEventChannelAdmin.SupplierAdmin._d_obtain_pull_consumer, args)

    __methods__ = [
        'obtain_push_consumer',
        'obtain_pull_consumer'] + CORBA.Object.__methods__

omniORB.registerObjref(SupplierAdmin._NP_RepositoryId, _objref_SupplierAdmin)
_0_CosEventChannelAdmin._objref_SupplierAdmin = _objref_SupplierAdmin
del SupplierAdmin
del _objref_SupplierAdmin
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class SupplierAdmin(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventChannelAdmin.SupplierAdmin._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'obtain_push_consumer': _0_CosEventChannelAdmin.SupplierAdmin._d_obtain_push_consumer,
        'obtain_pull_consumer': _0_CosEventChannelAdmin.SupplierAdmin._d_obtain_pull_consumer }

SupplierAdmin._omni_skeleton = SupplierAdmin
_0_CosEventChannelAdmin__POA.SupplierAdmin = SupplierAdmin
del SupplierAdmin
__name__ = 'twccommon.corba.CosEventChannelAdmin'
_0_CosEventChannelAdmin._d_EventChannel = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/CosEventChannelAdmin/EventChannel:1.0', 'EventChannel')
_0_CosEventChannelAdmin.EventChannel = omniORB.newEmptyClass()

class EventChannel:
    _NP_RepositoryId = _0_CosEventChannelAdmin._d_EventChannel[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_CosEventChannelAdmin.EventChannel = EventChannel
_0_CosEventChannelAdmin._tc_EventChannel = omniORB.tcInternal.createTypeCode(_0_CosEventChannelAdmin._d_EventChannel)
omniORB.registerType(EventChannel._NP_RepositoryId, _0_CosEventChannelAdmin._d_EventChannel, _0_CosEventChannelAdmin._tc_EventChannel)
EventChannel._d_for_consumers = ((), (_0_CosEventChannelAdmin._d_ConsumerAdmin,), None)
EventChannel._d_for_suppliers = ((), (_0_CosEventChannelAdmin._d_SupplierAdmin,), None)
EventChannel._d_destroy = ((), (), None)

class _objref_EventChannel(CORBA.Object):
    _NP_RepositoryId = EventChannel._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def for_consumers(self, *args):
        return _omnipy.invoke(self, 'for_consumers', _0_CosEventChannelAdmin.EventChannel._d_for_consumers, args)

    
    def for_suppliers(self, *args):
        return _omnipy.invoke(self, 'for_suppliers', _0_CosEventChannelAdmin.EventChannel._d_for_suppliers, args)

    
    def destroy(self, *args):
        return _omnipy.invoke(self, 'destroy', _0_CosEventChannelAdmin.EventChannel._d_destroy, args)

    __methods__ = [
        'for_consumers',
        'for_suppliers',
        'destroy'] + CORBA.Object.__methods__

omniORB.registerObjref(EventChannel._NP_RepositoryId, _objref_EventChannel)
_0_CosEventChannelAdmin._objref_EventChannel = _objref_EventChannel
del EventChannel
del _objref_EventChannel
__name__ = 'twccommon.corba.CosEventChannelAdmin__POA'

class EventChannel(PortableServer.Servant):
    _NP_RepositoryId = _0_CosEventChannelAdmin.EventChannel._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'for_consumers': _0_CosEventChannelAdmin.EventChannel._d_for_consumers,
        'for_suppliers': _0_CosEventChannelAdmin.EventChannel._d_for_suppliers,
        'destroy': _0_CosEventChannelAdmin.EventChannel._d_destroy }

EventChannel._omni_skeleton = EventChannel
_0_CosEventChannelAdmin__POA.EventChannel = EventChannel
del EventChannel
__name__ = 'twccommon.corba.CosEventChannelAdmin'
__name__ = 'twccommon.corba.twccommon.corba.CosEventChannelAdmin_idl'
__name__ = 'twccommon.corba.SimpleEventChannelAdmin'
_0_SimpleEventChannelAdmin = omniORB.openModule('twccommon.corba.SimpleEventChannelAdmin', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventChannelAdmin.idl')
_0_SimpleEventChannelAdmin__POA = omniORB.openModule('twccommon.corba.SimpleEventChannelAdmin__POA', '/n/azmo/ud2/jriley/se/personality/domestic/release/v1.14p1/upgrade/work/domestic_upgrade/work/autobuild/twc_lib-1.7_p1/pkg/work/twclib/src/pythonlib/twccommon/corba/../../../lib/twc_corba/CosEventChannelAdmin.idl')
_0_SimpleEventChannelAdmin._d_EventChannelFactory = (omniORB.tcInternal.tv_objref, 'IDL:omg.org/SimpleEventChannelAdmin/EventChannelFactory:1.0', 'EventChannelFactory')
_0_SimpleEventChannelAdmin.EventChannelFactory = omniORB.newEmptyClass()

class EventChannelFactory:
    _NP_RepositoryId = _0_SimpleEventChannelAdmin._d_EventChannelFactory[1]
    
    def __init__(self):
        raise RuntimeError('Cannot construct objects of this type.')

    _nil = CORBA.Object._nil

_0_SimpleEventChannelAdmin.EventChannelFactory = EventChannelFactory
_0_SimpleEventChannelAdmin._tc_EventChannelFactory = omniORB.tcInternal.createTypeCode(_0_SimpleEventChannelAdmin._d_EventChannelFactory)
omniORB.registerType(EventChannelFactory._NP_RepositoryId, _0_SimpleEventChannelAdmin._d_EventChannelFactory, _0_SimpleEventChannelAdmin._tc_EventChannelFactory)
EventChannelFactory._d_create_eventchannel = ((), (_0_CosEventChannelAdmin._d_EventChannel,), None)

class _objref_EventChannelFactory(CORBA.Object):
    _NP_RepositoryId = EventChannelFactory._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    
    def create_eventchannel(self, *args):
        return _omnipy.invoke(self, 'create_eventchannel', _0_SimpleEventChannelAdmin.EventChannelFactory._d_create_eventchannel, args)

    __methods__ = [
        'create_eventchannel'] + CORBA.Object.__methods__

omniORB.registerObjref(EventChannelFactory._NP_RepositoryId, _objref_EventChannelFactory)
_0_SimpleEventChannelAdmin._objref_EventChannelFactory = _objref_EventChannelFactory
del EventChannelFactory
del _objref_EventChannelFactory
__name__ = 'twccommon.corba.SimpleEventChannelAdmin__POA'

class EventChannelFactory(PortableServer.Servant):
    _NP_RepositoryId = _0_SimpleEventChannelAdmin.EventChannelFactory._NP_RepositoryId
    
    def __del__(self):
        if _omnipy is not None:
            _omnipy.releaseObjref(self)
        

    _omni_op_d = {
        'create_eventchannel': _0_SimpleEventChannelAdmin.EventChannelFactory._d_create_eventchannel }

EventChannelFactory._omni_skeleton = EventChannelFactory
_0_SimpleEventChannelAdmin__POA.EventChannelFactory = EventChannelFactory
del EventChannelFactory
__name__ = 'twccommon.corba.SimpleEventChannelAdmin'
__name__ = 'twccommon.corba.twccommon.corba.CosEventChannelAdmin_idl'
_exported_modules = ('twccommon.corba.CosEventChannelAdmin', 'twccommon.corba.CosEventComm', 'twccommon.corba.SimpleEventChannelAdmin')
