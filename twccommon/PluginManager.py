'''
Provides a plugin facility.  Plugins are simply modules that can loaded
dynamically at run time.  Since Python is an interpreted scripting language
dynamic code loading is easy.  However, this module provides an interface
to do request loading (and reloading if file is replaced).  It also provides
an interface to request a module from a string name, an interface to 
query whether or not a named plugin has been loaded, and an interface for
querying the list of loaded plugins.
'''
import os.path as os
import imp
import sys
import twccommon

class PluginManager:
    
    def __init__(self, pluginRoot, nameSpace = 'plugins'):
        self._root = pluginRoot
        self._nameSpace = nameSpace
        self._plugins = { }

    
    def _getPluginFileAttribs(self, pluginName):
        fdesc = None
        ftime = 0
        fl = [
            ('py', 'r', imp.PY_SOURCE),
            ('pyc', 'rb', imp.PY_COMPILED)]
        for fattr in fl:
            (ext, mode, type) = fattr
            fname = '%s/%s.%s' % (self._root, pluginName, ext)
            if not os.path.exists(fname):
                continue
            
            ft = os.path.getmtime(fname)
            if ft > ftime:
                ftime = ft
                fdesc = (fname, ftime, fattr)
            
        
        if fdesc == None:
            raise ImportError, 'cannot find plugin %s/%s' % (self._root, pluginName)
        
        return fdesc

    
    def _loadPlugin(self, pluginName, fname, ftime, fattr, initFnArgs):
        (ext, mode, type) = fattr
        plugin = twccommon.Data(mtime = ftime)
        qualifiedName = '%s_%s' % (self._nameSpace, pluginName)
        f = open(fname, mode)
        
        try:
            plugin.mod = imp.load_module(qualifiedName, f, fname, fattr)
            fn = getattr(plugin.mod, FN_INIT, None)
            if fn != None:
                apply(fn, initFnArgs)
            
            self._plugins[pluginName] = plugin
        finally:
            f.close()


    
    def _needsLoading(self, pluginName, ftime):
        load = 0
        
        try:
            plugin = self._plugins[pluginName]
            if ftime > plugin.mtime:
                load = 1
        except KeyError:
            load = 1

        return load

    
    def needsLoading(self, pluginName):
        '''Determine if the plugin file needs to be loaded (or reloaded).

        Parameters:
        - pluginName: The name of the plugin of interest.

        Return: 
            Returns true if either the plugin has not been loaded or
            if the plugin file has been replaced since it was last 
            loaded.
        '''
        (fname, ftime, fattr) = _getPluginFileAttribs(pluginName)
        return self._needsLoading(pluginName, ftime)

    
    def isPluginLoaded(self, pluginName):
        '''Indicates whether the specified plugin has been loaded.

        Parameters:
        - pluginName: The name of the plugin of interest.

        Return: 
        Returns true if the plugin has already been loaded.
        '''
        return self._plugins.has_key(pluginName)

    
    def getPluginModule(self, pluginName):
        '''Gets a module object for the specified plugin.
        No attempt is made to load (or reload) the module.

        It is an error to call this func. for a plugin that 
        has not been previously loaded.  The isPluginLoaded()
        function can be used as a test.

        Parameters:
        - pluginName: The name of the plugin of interest.

        Return: 
        Returns a ref. to the module corresponding to the plugin name.
        '''
        return self._plugins[pluginName].mod

    
    def loadPlugin(self, pluginName, initFnArgs = ()):
        """Load (or reload) the specified plugin.
        
        If the plugin module has not been loaded before, then it will 
        be imported.  Otherwise it will be reloaded.  No test is performed
        to determine if the plugin file has been updated.  See 
        retrievePlugin().

        If the module has defined a function named 'init', it will be
        exectued and initFnArgs specifies the parametes for the call.

        If the plugin cannot be loaded, then a corresponding exception 
        will be raised: IOError, ImportError, etc.

        Parameters:
        - pluginName: The name of the plugin of interest.
        - initFnArgs: Parameters passed when the plugin modules init fn
        is invoked.  Must be a tuple with an arity matching
        the number of params.  Defaults to no params (an empty tuple).

        Return: 
        Returns a ref. to the module corresponding to the plugin name.
        """
        (fname, ftime, fattrs) = self._getPluginFile(pluginName)
        self._loadPlugin(pluginName, fname, ftime, fattrs, initFnArgs)
        return self._plugins[pluginName].mod

    
    def retrievePlugin(self, pluginName, initFnArgs = ()):
        """Get a module object for the specified plugin.
        If the plugin module has not been loaded before, then it will 
        be imported.  If the plugin file is newer than the last time
        it was loaded, then it will be reloaded.

        If the module has defined a function named 'init', it will be
        exectued and initFnArgs specifies the parametes for the call.

        If the plugin cannot be loaded, then a corresponding exception 
        will be raised: IOError, ImportError, etc.

        Parameters:
        - pluginName: The name of the plugin of interest.
        - initFnArgs: Parameters passed when the plugin modules init fn
        is invoked.  Must be a tuple with an arity matching
        the number of params.  Defaults to no params (an empty tuple).

        Return: 
        Returns a ref. to the module corresponding to the plugin name.
        """
        (fname, ftime, fattrs) = self._getPluginFileAttribs(pluginName)
        load = self._needsLoading(pluginName, ftime)
        if load:
            self._loadPlugin(pluginName, fname, ftime, fattrs, initFnArgs)
        
        return self._plugins[pluginName].mod

    
    def getPlugins(self):
        '''Return a list of loaded plugins.

        Return: 
        Returns a list of references to the modules corresponding to all of
        the loaded plugins.
        '''
        list = []
        for p in self._plugins.values():
            list.append(p.mod)
        
        return list


FN_INIT = 'init'
