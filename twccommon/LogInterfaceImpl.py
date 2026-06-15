import syslog
from twccommon.Log import ERR
from twccommon.Log import WARN
from twccommon.Log import INFO
from twccommon.Log import DBG

class InterfaceImpl:
    '''Syslog implementation.'''
    
    def setIdent(self, ident):
        syslog.openlog(ident, syslog.LOG_PID, syslog.LOG_LOCAL1)

    
    def setLevel(self, level):
        self.level = level

    
    def critical(self, msg):
        syslog.syslog(syslog.LOG_CRIT, '[CRIT] ' + msg)

    
    def error(self, msg):
        if self.level >= ERR:
            syslog.syslog(syslog.LOG_ERR, '[ERR] ' + msg)
        

    
    def warning(self, msg):
        if self.level >= WARN:
            syslog.syslog(syslog.LOG_WARNING, '[warn] ' + msg)
        

    
    def info(self, msg):
        if self.level >= INFO:
            syslog.syslog(syslog.LOG_INFO, '[info] ' + msg)
        

    
    def debug(self, msg):
        if self.level >= DBG:
            syslog.syslog(syslog.LOG_DEBUG, '[dbg] ' + msg)
        


