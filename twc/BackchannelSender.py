import os
import time
import commands
import twccommon.Log as Log
import twc.dsmarshal as dsm
import twc.DataStoreInterface as ds

class BackchannelSender:
    '''Open the backchannel, transfer a file, and close the backchannel'''
    
    def __init__(self, file):
        self.fileToSend = file
        self._BackchannelSender__getDatastoreConfig()

    
    def __getDatastoreConfig(self):
        ds.init()
        self.tgtDir = dsm.defaultedGet('backchannDir', '/logs/backchannel')
        self.tgtAcct = dsm.defaultedGet('backchannAcct', 'dgadmin')
        self.tgtAddr = dsm.defaultedGet('backchannAddr', '65.212.71.50')
        ds.uninit()

    
    def __resetBackchannel(self):
        (rc, outLines) = commands.getstatusoutput('sudo prov_netconf 1')
        if rc:
            Log.error('backchannel reset: (rc=%d) %s' % (rc, outLines))
        

    
    def __openBackchannel(self):
        cmd = '/usr/local/bin/backchannel_up'
        (rc, outLines) = commands.getstatusoutput(cmd)
        if rc:
            Log.error('backchannel_up script: (rc=%d) %s' % (rc, outLines))
        else:
            Log.debug('backchannel_up script has opened the backchannel')

    
    def __setBackchannelDown(self):
        cmd = 'sudo /usr/local/bin/backchannel_down'
        (rc, outLines) = commands.getstatusoutput(cmd)
        if rc:
            Log.error('backchannel_down script: (rc=%d) %s' % (rc, outLines))
        else:
            Log.debug('backchannel_down script has closed the backchannel')

    
    def send(self, resetFlag):
        
        try:
            if len(self.fileToSend) == 0:
                Log.warning('filename is blank - pretend to succeed')
                return 1
            
            batchCmd = 'put ' + self.fileToSend + ' ' + self.tgtDir + '\n'
            self.batchFile = os.path.dirname(self.fileToSend) + '/sftpCommands.bat'
            fd = open(self.batchFile, 'w')
            fd.write(batchCmd)
            fd.close()
            cmd = "/usr/bin/sftp  -oBatchMode='yes' "
            cmd += '-oIdentityFile=~/.ssh/starlog_rsa   -b ' + self.batchFile
            cmd += ' ' + self.tgtAcct + '@' + self.tgtAddr
            if resetFlag == 1:
                Log.debug('Resetting backchannel  (replacing /etc/rc.conf)')
                self._BackchannelSender__resetBackchannel()
            
            self._BackchannelSender__openBackchannel()
            (rc, outLines) = commands.getstatusoutput(cmd)
            if rc:
                Log.error('Shell Cmd err: %s: %s' % (cmd, outLines))
                return 0
            else:
                Log.info('Sent file to %s@%s:%s' % (self.tgtAcct, self.tgtAddr, self.tgtDir))
                self.cleanup()
                return 1
        finally:
            self._BackchannelSender__setBackchannelDown()


    
    def cleanup(self):
        if os.path.isfile(self.batchFile):
            os.remove(self.batchFile)
        


