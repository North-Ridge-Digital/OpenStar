import time
import twc.Jobs as twc
import twc.dsmarshal as dsm
import twccommon.Log as Log
import twc.DataStoreInterface as ds

class StoredJob(twc.Jobs.Job):
    """copy a Job's run-time to the DataStore so it survives process restarts"""
    
    def __init__(self, jobName):
        self.dsName = 'job_' + jobName
        self.timet = 0
        twc.Jobs.Job.__init__(self, jobName)

    
    def scheduleIn(self, secondsFromNow):
        self.timet = time.time() + secondsFromNow
        twc.Jobs.Job.scheduleIn(self, secondsFromNow)

    
    def reschedule(self):
        Log.debug('saving timet to Datastore %s %d' % (self.dsName, self.timet))
        ds.init()
        dsm.set(self.dsName, self.timet, 0)
        ds.commit()
        ds.uninit()
        twc.Jobs.Job.reschedule(self)


