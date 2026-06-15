import os
import glob
import shutil
import twccommon.Log as Log
import twc.dsmarshal as dsm
import twc.DataStoreInterface as ds

def mkSubDir(dir, subdir):
    fullpath = dir + '/' + subdir
    if not os.path.isdir(fullpath):
        os.makedirs(fullpath)
    
    return fullpath + '/'


class FileSet:
    
    def __init__(self):
        pass

    
    def collect(self, tarDir):
        '''called every time FileSet gets a callback to re-collect the files'''
        pass

    
    def onSent(self):
        """fcn applied to original files after they've been successfully sent"""
        pass



class FileSetCmd(FileSet):
    
    def __init__(self, baseCmd, filename):
        self.cmd = baseCmd
        self.fname = filename

    
    def collect(self, tarDir):
        tarDir = mkSubDir(tarDir, 'cmd')
        cmd = self.cmd + ' > ' + tarDir + self.fname
        rc = os.system(cmd)
        if rc != 0:
            Log.error('%s; running cmd: %s' % (os.strerror(rc / 256), cmd))
        



class FileSetEncrypt(FileSet):
    
    def __init__(self, fileList, key = 'no_log_scrubbing_please'):
        self.files = fileList
        self.key = key

    
    def collect(self, tarDir):
        '''put encrypted versions of the files in our sub-directory'''
        tarDir = mkSubDir(tarDir, '/encrypt')
        baseCmd = '/usr/bin/bdes -k ' + self.key + ' < '
        for file in self.files:
            if not os.path.isfile(file):
                Log.error("%s isn't a file and will not be sent" % file)
            else:
                fname = os.path.basename(file)
                cmd = baseCmd + file + ' > ' + tarDir + fname + 'c'
                if os.system(cmd) != 0:
                    Log.error('Unable to run cmd: %s' % cmd)
                else:
                    Log.info('encrypted %s' % file)
        



class FileSetRunLogs(FileSet):
    
    def __init__(self, pattern):
        self.pattern = pattern

    
    def collect(self, tarDir):
        tarDir = mkSubDir(tarDir, '/runlogs')
        runLogs = glob.glob(self.pattern)
        self.renameList = []
        Log.info('collecting %d run logs' % len(runLogs))
        for file in runLogs:
            if os.path.isfile(file) == 0:
                Log.error("RunLog %s isn't a file and will not be sent" % file)
            else:
                self.renameList.append(file)
                
                try:
                    fname = os.path.basename(file)
                    shutil.copy(file, tarDir + fname)
                except e:
                    Log.error('%s; failed to copy: %s' % (str(e), file))

        

    
    def onSent(self):
        for file in self.renameList:
            os.rename(file, file + '.sent')
        



class FileSetDatastore(FileSet):
    
    def __init__(self, keyList, outputFileName = 'datastore.vals'):
        self.keyList = keyList
        self.fname = outputFileName

    
    def collect(self, tarDir):
        fd = open(tarDir + '/' + self.fname, 'a')
        ds.init()
        for key in self.keyList:
            val = dsm.defaultedGet(key, 'Unknown')
            fd.write('%s = %s\n' % (key, repr(val)))
        
        ds.uninit()
        fd.close()

    
    def updateKeyList(self, keyList):
        self.keyList = keyList



class FileSetDatastoreIndirect(FileSetDatastore):
    
    def __init__(self, key, outputFileName = 'datastore.vals'):
        self.key = key
        FileSetDatastore.__init__(self, [], outputFileName)

    
    def collect(self, tarDir):
        ds.init()
        newKeyList = dsm.defaultedGet(self.key, None)
        ds.uninit()
        if newKeyList:
            if isinstance(newKeyList, list) and len(newKeyList) > 0:
                FileSetDatastore.updateKeyList(self, newKeyList)
                FileSetDatastore.collect(self, tarDir)
            
        


