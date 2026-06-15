"""A simple function scheduler.
Used to invoke callables (functions, methods, class instances, etc.)
at specified times.  Callback times can be set at a standard 'daily' time
or as a number of seconds from the present time.  Callbacks are executed
once and then removed from the internal event list.  In order to achieve
repeating callbacks, the application must explicitly call reschedule().
"""
import sys
import time
import traceback
import twccommon
import twccommon.Log as Log
import twccommon.IOCatcher as IOCatcher
_events = []

class _Event:
    
    def __init__(self, t, fn, params):
        self.time = t
        self.fn = fn
        self.params = params



def restlessSleep(totalSleep):
    cycleTime = 1
    sleepCycles = totalSleep / cycleTime
    while sleepCycles > 0:
        time.sleep(cycleTime)
        sleepCycles -= 1


def mainloop():
    '''Begin scheduler processing, i.e. invoke callbacks at scheduled times.
    Runs until no more events are scheduled.
    '''
    global _events
    while _events:
        
        try:
            event = _events[0]
            t = event.time - time.time()
            if t <= 0:
                _events = _events[1:]
                apply(event.fn, event.params)
            else:
                restlessSleep(t)
        except SystemExit:
            raise 
        except:
            Log.logCurrentException("Scheduler ran an Event that didn't catch its exception:")



def _schedule(t, fn, params):
    if not callable(fn):
        raise RuntimeError, 'Cannot schedule a non-callable object'
    
    event = _Event(t, fn, params)
    _events.append(event)
    _events.sort((lambda e1, e2: twccommon.compare(e1.time, e2.time)))


def execIn(seconds, fn, params = ()):
    '''Schedule an event to run some number of seconds from now.'''
    t = time.time()
    t = t + seconds
    _schedule(t, fn, params)


def hasValidDay(wdl):
    '''does the input week-day-list contain at least one valid week day?'''
    for d in wdl:
        if d in [
            0,
            1,
            2,
            3,
            4,
            5,
            6]:
            return 1
        
    
    return 0


def execAt(hour, minute, second, daysOfWeek, fn, params = ()):
    '''Schedule an event at a standard time on certain days of the week.
    If the specified time is already past, then the event is
    scheduled for the same time tomorrow.
    '''
    t = time.time()
    (Y, M, D, h, m, s, wd, d, dst) = time.localtime(t)
    next = time.mktime((Y, M, D, hour, minute, second, wd, d, dst))
    if next >= t and wd in daysOfWeek:
        _schedule(next, fn, params)
    
    if next < t or wd not in daysOfWeek:
        if hasValidDay(daysOfWeek) == 0:
            raise RuntimeError, 'need a valid list of days! (%s)' % daysOfWeek
        
        nextDay = wd + 1
        while nextDay % 7 not in daysOfWeek:
            nextDay = nextDay + 1
        next = next + (nextDay - wd) * 24 * 3600
        (Y, M, D, h, m, s, wd, d, dst) = time.localtime(next)
        next = time.mktime((Y, M, D, hour, m, s, wd, d, -1))
        _schedule(next, fn, params)
    

