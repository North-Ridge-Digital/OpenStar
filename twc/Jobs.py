import traceback
import twccommon.Scheduler as Scheduler
import twccommon.Log as Log
import twccommon.IOCatcher as IOCatcher
import twccommon.corba as twccommon
import omniORB.CORBA as CORBA
import CosNaming
_ctx = 0
_consumer = 0
_tc = 0
_jobList = []

def init(corbaArgs):
    global _ctx, _ctx
    
    try:
        orb = CORBA.ORB_init(corbaArgs, CORBA.ORB_ID)
        twccommon.corba.setOrb(orb)
        _ctx = orb.resolve_initial_references('NameService')
        _ctx = _ctx._narrow(CosNaming.NamingContext)
    except:
        Log.critical("Can't find Name Service, check that nsd is running")
        logStackTrace()
        return -1



def logStackTrace():
    maxNumExceptions = 3
    writeToSyslog = IOCatcher.IOLogger(Log.critical)
    traceback.print_exc(maxNumExceptions, writeToSyslog)


def addJob(job):
    _jobList.append(job)


def getJobList():
    return _jobList


def setJobList(jobList):
    global _jobList
    _jobList = jobList


class Job:
    '''A Job knows how to schedule itself for execution'''
    
    def __init__(self, jobName):
        self._Job__jobName = jobName
        self._Job__frequency = 0
        self._Job__dailyHour = 0
        self._Job__dailyMinute = 0
        self._Job__dailySecond = 0
        self._Job__dailyFlag = 0
        self._Job__dayList = []
        self._Job__error = 0
        self._Job__errorReported = 0
        addJob(self)

    
    def info(self, msg):
        Log.info('%s: %s' % (self._Job__jobName, msg))

    
    def warn(self, msg):
        Log.warning('%s: %s' % (self._Job__jobName, msg))

    
    def error(self, msg):
        Log.error('%s: %s' % (self._Job__jobName, msg))

    
    def crit(self, msg):
        Log.critical('%s: %s' % (self._Job__jobName, msg))

    
    def scheduleIn(self, seconds):
        self._Job__frequency = seconds

    
    def scheduleAt(self, hour, minute, second):
        self._Job__dailyHour = hour
        self._Job__dailyMinute = minute
        self._Job__dailySecond = second
        everyDay = [
            0,
            1,
            2,
            3,
            4,
            5,
            6]
        self._Job__dayList = everyDay
        self._Job__dailyFlag = 1

    
    def preExec(self):
        '''set a prefix for all of the log messages produced by this Job'''
        if self._Job__jobName != None:
            Log.setPrefix(self._Job__jobName)
            Log.debug('log prefix set')
        

    
    def postExec(self):
        Log.clearPrefix()

    
    def execute(self):
        '''implemented by derived classes'''
        pass

    
    def __call__(self):
        '''entry point from Python Scheduler'''
        Log.debug('Executing ' + self._Job__jobName + ' (' + self.getParams() + ')')
        self.preExec()
        self.execute()
        self.postExec()
        return None

    
    def getParams(self):
        return ''

    
    def getJobName(self):
        return self._Job__jobName

    
    def getFrequency(self):
        return self._Job__frequency

    
    def getDailyFlag(self):
        return self._Job__dailyFlag

    
    def getDailyHour(self):
        return self._Job__dailyHour

    
    def getDailyMinute(self):
        return self._Job__dailyMinute

    
    def getDailySecond(self):
        return self._Job__dailySecond

    
    def getDailyHourMinSec(self):
        return (self._Job__dailyHour, self._Job__dailyMinute, self._Job__dailySecond)

    
    def getDayOfWeekList(self):
        return self._Job__dayList

    
    def getError(self):
        return self._Job__error

    
    def setError(self):
        self._Job__error = 1

    
    def clearError(self):
        self._Job__error = 0

    
    def getErrorReported(self):
        return self._Job__errorReported

    
    def setErrorReported(self):
        self._Job__errorReported = 1

    
    def clearErrorReported(self):
        self._Job__errorReported = 0

    
    def reschedule(self):
        if self._Job__dailyFlag == 1:
            Scheduler.execAt(self._Job__dailyHour, self._Job__dailyMinute, self._Job__dailySecond, [
                0,
                1,
                2,
                3,
                4,
                5,
                6], self)
        else:
            Scheduler.execIn(self._Job__frequency, self)


