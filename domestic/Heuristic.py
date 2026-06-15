import twccommon
DISP_POS = 0
PRI_POS = 1
PRODNM_POS = 2
PRODPG_POS = 3
PROD_POS = 4
CUR_POS = 5
DES_POS = 6
OPT_POS = 7
MAX_POS = 8
MIN_POS = 9
STEP_POS = 10
EXCL_POS = 11

def displayOrder(lst1, lst2):
    return twccommon.compare(lst1[DISP_POS], lst2[DISP_POS])


def priorityDisplayOrder(lst1, lst2):
    result = twccommon.compare(lst1[PRI_POS], lst2[PRI_POS])
    if result:
        return result
    else:
        return twccommon.compare(lst1[DISP_POS], lst2[DISP_POS])


class Heuristic:
    
    def __init__(self, config):
        self._config = config
        self._srcList = []
        self._runList = []

    
    def debugProdEntry(self, pe):
        twccommon.Log.debug('%3d %3d %25s %4d %3d %3d %3d %3d %3d %3d %3d' % (pe[DISP_POS], pe[PRI_POS], pe[PRODNM_POS], pe[PRODPG_POS], pe[CUR_POS], pe[DES_POS], pe[OPT_POS], pe[MAX_POS], pe[MIN_POS], pe[STEP_POS], pe[EXCL_POS]))

    
    def debug(self, list, msg = ''):
        if len(msg):
            twccommon.Log.debug(msg)
        
        twccommon.Log.debug('DSP PRI          Product          Page CUR DES OPT MAX MIN STP EXC')
        for pe in list:
            self.debugProdEntry(pe)
        

    
    def load(self, srcList, duration, dynamicPlaylist):
        raise Exception('load heuristic not implemented')

    
    def reduce(self, curDuration, srcList, runList, duration, dynamicPlaylist):
        raise Exception('over heuristic not implemented')

    
    def grow(self, curDuration, srcList, runList, duration, dynamicPlaylist):
        raise Exception('under heuristic not implemented')

    
    def sortDisplay(self, list):
        list.sort(displayOrder)

    
    def sortPriorityDisplay(self, list):
        list.sort(priorityDisplayOrder)

    
    def isExclusiveInList(self, exclusive, list):
        result = 0
        if exclusive:
            for pe in list:
                if pe[EXCL_POS] == exclusive:
                    result = 1
                    break
                
            
        
        return result


