import os
import time
import twccommon.Log as Log
import twc.dsmarshal as dsm
import twc.DataStoreInterface as ds

class Archive:
    '''create a single tar-file archive composed of several sets of files'''
    
    def __init__(self, dir):
        self.tarDir = dir
        self.tarfile = None
        self.filesets = []

    
    def addFileSets(self, filesetList):
        '''add the fileset-list passed in as an arg to our master list'''
        for fileset in filesetList:
            self.filesets.append(fileset)
        

    
    def build(self):
        '''build a single tarfile from all the files found in tarDir'''
        timeStr = str(int(time.time()))
        self._Archive__getDatastoreConfig()
        if self.pers == 'domestic':
            pfx = 'dom.'
        elif self.pers == 'wxscan':
            pfx = 'wxs.'
        elif self.pers == 'dbs':
            pfx = 'dbs.'
        else:
            pfx = ''
        if not os.path.isdir(self.tarDir):
            os.makedirs(self.tarDir)
        
        for fileset in self.filesets:
            fileset.collect(self.tarDir)
        
        tarfile = os.path.dirname(self.tarDir) + '/' + pfx + self.starId + '.' + timeStr + '.iStar.tgz'
        self.tarfile = tarfile
        os.chdir(self.tarDir)
        cmd = '/usr/bin/tar -czf ' + tarfile + ' .'
        rc = os.system(cmd)
        if rc != 0:
            Log.error('%s: running cmd: %s' % (os.strerror(rc / 256), cmd))
            return ''
        
        return tarfile

    
    def onSent(self):
        for fileset in self.filesets:
            fileset.onSent()
        

    
    def clear(self):
        '''delete all files in the tar-dir, and the tar-file itself'''
        os.chdir('/tmp')
        self._Archive__deleteRecursive(self.tarDir)
        if self.tarfile:
            os.remove(self.tarfile)
            self.tarfile = None
        

    
    def __deleteRecursive(self, baseDir):
        '''Delete all files & sub-dirs beneath some base dir.  Leave base'''
        Log.debug('deleting all files and subdirs below %s' % self.tarDir)
        if not os.path.isdir(baseDir):
            return None
        
        for file in os.listdir(baseDir):
            fullpath = os.path.join(baseDir, file)
            if os.path.isfile(fullpath):
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                self._Archive__deleteRecursive(fullpath)
                os.rmdir(fullpath)
            
        

    
    def __getDatastoreConfig(self):
        ds.init()
        self.starId = dsm.defaultedConfigGet('starId', 'missing')
        self.pers = dsm.defaultedGet('personality', 'missing')
        ds.uninit()


