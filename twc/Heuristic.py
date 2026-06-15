import twccommon
DISP_POS = 0
PRI_POS = 1
PRODNM_POS = 2
PRODINST_POS = 3
PRODPG_POS = 4
PROD_POS = 5
CUR_POS = 6
DES_POS = 7
OPT_POS = 8
MAX_POS = 9
MIN_POS = 10
STEP_POS = 11
EXCL_POS = 12
CPLISTS_POS = 13

def displayOrder(lst1, lst2):
    return twccommon.compare(lst1[DISP_POS], lst2[DISP_POS])


def priorityDisplayOrder(lst1, lst2):
    result = twccommon.compare(lst1[PRI_POS], lst2[PRI_POS])
    if result:
        return result
    else:
        return twccommon.compare(lst1[DISP_POS], lst2[DISP_POS])


class Heuristic:
    
    def __init__(self):
        self._srcList = []
        self._runList = []

    
    def debugProdEntry(self, pe):
        twccommon.Log.debug('%3d %3d %25s %4d %4d %3d %3d %3d %3d %3d %3d %3d' % (pe[DISP_POS], pe[PRI_POS], pe[PRODNM_POS], pe[PRODINST_POS], pe[PRODPG_POS], pe[CUR_POS], pe[DES_POS], pe[OPT_POS], pe[MAX_POS], pe[MIN_POS], pe[STEP_POS], pe[EXCL_POS]))

    
    def debug(self, list, msg = ''):
        if len(msg):
            twccommon.Log.debug(msg)
        
        twccommon.Log.debug('DSP PRI          Product          Inst Page CUR DES OPT MAX MIN STP EXC')
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



class loadPriority_v1(Heuristic):
    
    def __init__(self):
        Heuristic.__init__(self)

    
    def load(self, srcList, duration, dynPlist):
        runList = []
        curDuration = 0
        self.sortPriorityDisplay(srcList)
        while 1:
            (prodDuration, srcList, runList) = self._loadProduct(duration, dynPlist, srcList, runList)
            curDuration += prodDuration
            if prodDuration == 0 or curDuration >= duration:
                break
            
        return (curDuration, srcList, runList)

    
    def _skipPriority(self, priority):
        return 0

    
    def _loadProduct(self, duration, dynPlist, srcList, runList):
        found = 0
        prodDuration = 0
        newSrcList = []
        for pe in srcList:
            if found and self.isExclusiveInList(pe[EXCL_POS], runList) or self._skipPriority(pe[PRI_POS]):
                newSrcList.append(pe)
                continue
            
            prod = dynPlist.getProduct(pe[PRODNM_POS], pe[PRODINST_POS])
            if prod == None:
                twccommon.Log.info("unable to load product '%s'" % pe[PRODNM_POS])
                continue
            
            if pe[PRODPG_POS]:
                if pe[PROD_POS]:
                    prodDuration = pe[DES_POS]
                else:
                    tmpList = []
                    for entry in srcList:
                        if entry[PRODNM_POS] == pe[PRODNM_POS]:
                            tmpList.append((entry[PRODPG_POS], entry[MIN_POS], entry[MAX_POS], entry[OPT_POS]))
                        
                    
                    pages = prod.getDesiredPageDurations(tmpList)
                    for entry in srcList:
                        if entry[PRODNM_POS] == pe[PRODNM_POS]:
                            entry[PROD_POS] = prod
                            entry[DES_POS] = pages[entry[PRODPG_POS] - 1]
                        
                    
                    prodDuration = pe[DES_POS]
            else:
                prodDuration = prod.getDesiredDuration(pe[MIN_POS], pe[MAX_POS], pe[OPT_POS])
            if prodDuration:
                if prodDuration <= pe[MAX_POS] and prodDuration >= pe[MIN_POS]:
                    pe[PROD_POS] = prod
                    pe[CUR_POS] = prodDuration
                    pe[DES_POS] = prodDuration
                    runList.append(pe)
                    self.debug(runList, 'runlist during load():')
                    found = 1
                    if pe[PRODPG_POS]:
                        twccommon.Log.info("%d desired duration - product '%s.%d'" % (prodDuration, pe[PRODNM_POS], pe[PRODPG_POS]))
                    else:
                        twccommon.Log.info("%d desired duration - product '%s'" % (prodDuration, pe[PRODNM_POS]))
                elif pe[PRODPG_POS]:
                    twccommon.Log.info("invalid desired duration(%d) max(%d) min(%d) - product '%s.%d'" % (prodDuration, pe[MAX_POS], pe[MIN_POS], pe[PRODNM_POS], pe[PRODPG_POS]))
                else:
                    twccommon.Log.info("invalid desired duration(%d) max(%d) min(%d) - product '%s'" % (prodDuration, pe[MAX_POS], pe[MIN_POS], pe[PRODNM_POS]))
            elif pe[PRODPG_POS]:
                twccommon.Log.info("zero desired duration - product '%s.%d'" % (pe[PRODNM_POS], pe[PRODPG_POS]))
            else:
                twccommon.Log.info("zero desired duration - product '%s'" % pe[PRODNM_POS])
        
        return (prodDuration, newSrcList, runList)



class loadPriorityOneOnly_v1(loadPriority_v1):
    
    def __init__(self):
        loadPriority_v1.__init__(self)

    
    def _skipPriority(self, priority):
        if priority == 1:
            return 0
        else:
            return 1



class overPriority_v1(Heuristic):
    
    def __init__(self):
        Heuristic.__init__(self)

    
    def reduce(self, curDuration, srcList, runList, duration, dynPlist):
        self._srcList = srcList
        self.sortPriorityDisplay(runList)
        runList.reverse()
        self._runList = runList
        curDuration = self._reduceByStepping(curDuration, duration)
        if curDuration > duration:
            curDuration = self._reduceByRemovingProducts(curDuration, duration)
        
        return (curDuration, self._srcList, self._runList)

    
    def _reduceByStepping(self, curDuration, duration):
        zeroDuration = 0
        while curDuration > duration:
            adjusted = 0
            curPri = -1
            for pe in self._runList:
                if pe[CUR_POS] - pe[STEP_POS] >= pe[MIN_POS] and pe[STEP_POS]:
                    if curPri == -1:
                        curPri = pe[PRI_POS]
                    
                    if pe[PRI_POS] != curPri:
                        break
                    
                    if curDuration <= duration:
                        break
                    
                    pe[CUR_POS] -= pe[STEP_POS]
                    if pe[CUR_POS] == 0:
                        zeroDuration = 1
                    
                    curDuration -= pe[STEP_POS]
                    adjusted = 1
                    self.debug(self._runList, 'runlist during reduce():')
                
            
            if adjusted == 0:
                break
            
        if zeroDuration:
            newRunList = []
            for pe in self._runList:
                if pe[CUR_POS]:
                    newRunList.append(pe)
                
            
            self._runList = newRunList
        
        return curDuration

    
    def _reduceByRemovingProducts(self, curDuration, duration):
        while curDuration > duration:
            adjusted = 0
            runListLen = len(self._runList)
            if runListLen:
                pe = self._runList[0]
                curDuration -= pe[CUR_POS]
                adjusted = 1
                newRunList = self._runList[1:]
                self._runList = newRunList
                self.debug(self._runList, 'runlist during reduce():')
            else:
                break
        return curDuration



class underPriority_v1(Heuristic):
    
    def __init__(self):
        Heuristic.__init__(self)

    
    def grow(self, curDuration, srcList, runList, duration, dynPlist):
        self.sortPriorityDisplay(srcList)
        self._srcList = srcList
        self.sortPriorityDisplay(runList)
        self._runList = runList
        curDuration = self._growByStepping(curDuration, duration)
        if curDuration < duration:
            curDuration = self._growByAddingProducts(curDuration, duration, dynPlist)
        
        return (curDuration, self._srcList, self._runList)

    
    def _growByStepping(self, curDuration, duration):
        while curDuration < duration:
            adjusted = 0
            curPri = -1
            for pe in self._runList:
                if pe[CUR_POS] + pe[STEP_POS] <= pe[MAX_POS] and pe[STEP_POS]:
                    if curPri == -1:
                        curPri = pe[PRI_POS]
                    
                    if pe[PRI_POS] != curPri:
                        break
                    
                    if curDuration >= duration:
                        break
                    
                    pe[CUR_POS] += pe[STEP_POS]
                    curDuration += pe[STEP_POS]
                    adjusted = 1
                    self.debug(self._runList, 'runlist during grow():')
                
            
            if adjusted == 0:
                break
            
        return curDuration

    
    def _growByAddingProducts(self, curDuration, duration, dynPlist):
        while curDuration < duration:
            adjusted = 0
            newSrcList = []
            for pe in self._srcList:
                if adjusted or self.isExclusiveInList(pe[EXCL_POS], self._runList):
                    newSrcList.append(pe)
                    continue
                
                prod = dynPlist.getProduct(pe[PRODNM_POS], pe[PRODINST_POS])
                if prod == None:
                    twccommon.Log.info("unable to load product '%s'" % pe[PRODNM_POS])
                    continue
                
                if pe[PRODPG_POS]:
                    if pe[PROD_POS]:
                        prodDuration = pe[DES_POS]
                    else:
                        tmpList = []
                        for entry in self._srcList:
                            if entry[PRODNM_POS] == pe[PRODNM_POS]:
                                tmpList.append((entry[PRODPG_POS], entry[MIN_POS], entry[MAX_POS], entry[OPT_POS]))
                            
                        
                        pages = prod.getDesiredPageDurations(tmpList)
                        for entry in self._srcList:
                            if entry[PRODNM_POS] == pe[PRODNM_POS]:
                                entry[PROD_POS] = prod
                                entry[DES_POS] = pages[entry[PRODPG_POS] - 1]
                            
                        
                        prodDuration = pe[DES_POS]
                else:
                    prodDuration = prod.getDesiredDuration(pe[MIN_POS], pe[MAX_POS], pe[OPT_POS])
                if prodDuration:
                    if prodDuration <= pe[MAX_POS] and prodDuration >= pe[MIN_POS]:
                        pe[PROD_POS] = prod
                        pe[CUR_POS] = prodDuration
                        pe[DES_POS] = prodDuration
                        curDuration += prodDuration
                        self._runList.append(pe)
                        self.debug(self._runList, 'runlist during grow():')
                        adjusted = 1
                        if pe[PRODPG_POS]:
                            twccommon.Log.info("%d desired duration - product '%s.%d'" % (prodDuration, pe[PRODNM_POS], pe[PRODPG_POS]))
                        else:
                            twccommon.Log.info("%d desired duration - product '%s'" % (prodDuration, pe[PRODNM_POS]))
                    elif pe[PRODPG_POS]:
                        twccommon.Log.info("invalid desired duration(%d) max(%d) min(%d) - product '%s.%d'" % (prodDuration, pe[MAX_POS], pe[MIN_POS], pe[PRODNM_POS], pe[PRODPG_POS]))
                    else:
                        twccommon.Log.info("invalid desired duration(%d) max(%d) min(%d) - product '%s'" % (prodDuration, pe[MAX_POS], pe[MIN_POS], pe[PRODNM_POS]))
                elif pe[PRODPG_POS]:
                    twccommon.Log.info("zero desired duration - product '%s.%d'" % (pe[PRODNM_POS], pe[PRODPG_POS]))
                else:
                    twccommon.Log.info("zero desired duration - product '%s'" % pe[PRODNM_POS])
            
            self._srcList = newSrcList
            if adjusted == 0:
                break
            
        return curDuration


