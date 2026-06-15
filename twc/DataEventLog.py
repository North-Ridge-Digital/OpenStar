import twccommon
import EventLog

class DataEventLog(EventLog.EventLog):
    
    def __init__(self, workfile, debug):
        self.debug = debug
        self.workFile = workfile
        self._DataEventLog__logMap = { }

    
    def writeData(self, tag, event):
        if self.debug == 1:
            self._writeData(tag, event)
        

    
    def _open(self):
        return file(self.workFile, 'w')


