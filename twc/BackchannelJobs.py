import time
import commands
import whrandom
import twc.Jobs as twc
import twc.StoredJobs as twc
import twccommon.Log as Log
import twc.dsmarshal as dsm
import twc.DataStoreInterface as ds
import twc.BackchannelSender as BackchannelSender
from twccommon import Scheduler

class BackchannelJob(twc.StoredJobs.StoredJob):
    '''Job Scheduler entry point to manage a backchannel transmission'''
    
    def __init__(self, archiv, jobName = 'BackChann', retryDelay = 600, retryCnt = 3):
        twc.StoredJobs.StoredJob.__init__(self, jobName)
        self.sender = None
        self.archiv = archiv
        self.retryDelay = retryDelay
        self.retryCntOrig = retryCnt
        self.retriesRemaining = retryCnt
        dsName = 'job_' + jobName
        runTime = self.getDatastoreRuntime(dsName)
        if runTime == 0:
            Log.debug('no run time found in Datastore for %s' % dsName)
            runTime = self._BackchannelJob__pickRuntimeTomorrow()
        else:
            Log.debug('retrieved run time from Datastore')
        self.scheduleRun(runTime)

    
    def getDatastoreRuntime(self, dsName):
        ds.init()
        timet = dsm.defaultedGet(dsName, 0)
        ds.uninit()
        return timet

    
    def scheduleRun(self, timet):
        offset = timet - time.time()
        if offset < 0:
            Log.debug('Datastore runtime was %s sec ago: Resched' % offset)
            timet = self._BackchannelJob__pickRuntimeTomorrow()
            offset = timet - time.time()
        
        (y, mo, d, h, m, s, wkday, doy, dst) = time.localtime(timet)
        Log.info('initial run at %02d:%02d:%02d on %d/%d. (%ds from now)' % (h, m, s, mo, d, offset))
        self.scheduleIn(offset)

    
    def getParams(self):
        return 'retry %dx, every %ds' % (self.retryCntOrig, self.retryDelay)

    
    def execute(self):
        '''called indirectly by the Scheduler from Jobs.Job.__call__()'''
        
        try:
            sendFlag = self._BackchannelJob__shouldSend()
            if sendFlag == 0:
                self._BackchannelJob__reSched()
                return None
            
            if self.retriesRemaining == self.retryCntOrig:
                self.tarfile = self.archiv.build()
                Log.info('created tarfile from Archive %s' % self.tarfile)
            
            self.sender = BackchannelSender.BackchannelSender(self.tarfile)
            self.sent = self.sender.send(self.resetFlag)
            self.retriesRemaining -= 1
            if self.sent:
                self.archiv.onSent()
                self._BackchannelJob__reSched()
            else:
                self._BackchannelJob__retry()
        except:
            Log.error('BackchannelJob.execute() is rescheduling on error')
            self._BackchannelJob__reSched()
            raise 


    
    def __reSched(self):
        self.retriesRemaining = self.retryCntOrig
        timet = self._BackchannelJob__pickRuntimeTomorrow()
        self.scheduleIn(timet - time.time())
        self.reschedule()
        (y, mo, d, h, m, s, wkday, doy, dst) = time.localtime(timet)
        Log.info('next run at %02d:%02d:%02d on %d/%d' % (h, m, s, mo, d))
        self.archiv.clear()
        if self.sender:
            self.sender.cleanup()
        
        self.tarfile = ''

    
    def __retry(self):
        if self.retriesRemaining > 0:
            Log.info('tarfile not sent, retry in %ds, %d more times' % (self.retryDelay, self.retriesRemaining))
            Scheduler.execIn(self.retryDelay, self)
        else:
            self._BackchannelJob__reSched()
            Log.warning('tarfile not sent, retry cnt is zero.  Give up.')

    
    def __pickRuntimeTomorrow(self):
        maxOffset = int(2.5 * 3600)
        minOffset = 600
        secAfterMidnite = minOffset + whrandom.randint(minOffset, maxOffset)
        (y, mo, d, h, m, s, wkday, doy, dst) = time.localtime(time.time())
        midNite = time.mktime((y, mo, d, 24, 0, 0, wkday, doy, dst))
        return midNite + secAfterMidnite

    
    def __shouldSend(self):
        ds.init()
        ver = dsm.getConfigVersion()
        resetAndSendKey = 'productionMachine'
        sendOnlyKey = 'backchannSendNoReset'
        sendFlag = 0
        resetAndSendFlag = int(dsm.defaultedGet(resetAndSendKey, 0))
        sendOnlyFlag = int(dsm.defaultedGet(sendOnlyKey, 0))
        ds.uninit()
        if sendOnlyFlag == 1 or resetAndSendFlag == 1:
            sendFlag = 1
            self.resetFlag = 1
        
        if resetAndSendFlag == 0:
            self.resetFlag = 0
        
        if sendOnlyFlag == 1 and resetAndSendFlag == 1:
            Log.warning('Conflict!  Both %s and %s are set.  Will Reset' % (sendOnlyKey, resetAndSendKey))
        
        explain = '%s=%s,  %s=%s  => sendFlag=%s.' % (sendOnlyKey, sendOnlyFlag, resetAndSendKey, resetAndSendFlag, sendFlag)
        if sendFlag == 0:
            Log.warning('%s  NOT sending any backchannel logs' % explain)
        else:
            Log.debug('%s  Will attempt to send backchannel logs' % explain)
        return sendFlag

    
    def postExec(self):
        twc.Jobs.Job.postExec(self)


