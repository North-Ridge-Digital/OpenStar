import libxml2
import libxslt
import string
import twc.DataStoreInterface as ds
import twc.dsmarshal as dsm
import twc.psp as twc
import twccommon
import xml.dom.minidom as xml

class Product:
    
    def __init__(self, params):
        self._Product__duration = 0
        self._Product__rs = None
        self._Product__pres = None
        self._Product__pageDurations = []
        self._Product__params = params
        self._Product__data = twc.Data()
        self._Product__testData = twc.Data()
        self._Product__label = []

    
    def getName(self):
        return self._Product__params.product

    
    def getProdInstance(self):
        return self._Product__params.prodInst

    
    def getShortName(self):
        return self._Product__params.prodName

    
    def getType(self):
        return self._Product__params.prodType

    
    def getParams(self):
        return self._Product__params

    
    def updateParams(self, other = None, **params):
        self._Product__params.update(other, **params)

    
    def getTestData(self):
        return self._Product__testData

    
    def updateTestData(self, other = None, **params):
        self._Product__testData.update(other, **params)

    
    def getData(self):
        return self._Product__data

    
    def updateData(self, other = None, **params):
        self._Product__data.update(other, **params)

    
    def getDuration(self):
        return self._Product__duration

    
    def setDuration(self, duration):
        self._Product__duration = duration

    
    def getDesiredDuration(self, minimum, maximum, optimal):
        if self.active():
            return self._getDesiredDuration(minimum, maximum, optimal)
        else:
            return 0

    
    def getDesiredPageDurations(self, pageParams):
        if self.active():
            return self._getDesiredPageDurations(pageParams)
        else:
            return [
                0] * len(pageParams)

    
    def getPageDurations(self):
        return self._Product__pageDurations

    
    def setPageDurations(self, durations):
        self._Product__pageDurations = durations

    
    def getLabel(self):
        return self._Product__label

    
    def setLabel(self, label):
        self._Product__label = label

    
    def addLabel(self, label, duration, image = None):
        d = twc.Data(label = label, duration = duration, image = image)
        self._Product__label.append(d)

    
    def active(self):
        return 1

    
    def loadData(self):
        self._loadData()

    
    def setRenderScript(self, rs):
        self._Product__rs = rs

    
    def setPresentation(self, pres):
        self._Product__pres = pres

    
    def genRenderScript(self, layerName, pspIncludePath = None, **ns):
        ns = twc.buildPyNamespace(default = ns, params = self._Product__params, prod = self)
        if self._Product__rs:
            self._Product__params.layerName = layerName
            rsc = twc.psp.evalPage(self._Product__rs, ns, pspIncludePath)
            return rsc
        elif self._Product__pres:
            return twc.presToRenderScript(self._Product__pres, layerName, **ns)
        else:
            return None

    
    def _getDesiredDuration(self, minimum, maximum, optimal):
        return optimal

    
    def _getDesiredPageDurations(self, pageParams):
        raise Exception('Multipage support not enabled for this product')

    
    def _loadData(self):
        pass



class DeactivateableProduct(Product):
    
    def active(self):
        pname = self.getName()
        fname = 'active%s' % (pname,)
        active = getattr(self.getParams(), fname, 1)
        return active



class ProductLoader:
    
    def __init__(self):
        self._ProductLoader__prodMap = { }

    
    def startProdType(self, prodType):
        pass

    
    def loadProduct(self, prodType, prodName, prodInst):
        pass

    
    def loadProductFile(self, fname, params):
        
        try:
            (prodClass, rs, pres) = self._ProductLoader__prodMap[fname]
        except KeyError:
            (prodClass, rs, pres) = self._loadProductFile(fname)
            self._ProductLoader__prodMap[fname] = (prodClass, rs, pres)

        return self._makeProduct(prodClass, rs, pres, params)

    
    def flush(self):
        self._ProductLoader__prodMap.clear()

    
    def _makeProduct(self, prodClass, rs, pres, params):
        prod = prodClass(params)
        if rs:
            prod.setRenderScript(rs)
        elif pres:
            prod.setPresentation(pres)
        
        if prod.active():
            prod.loadData()
        else:
            prod = None
        return prod

    
    def _parseProductDoc(self, doc):
        dom = None
        
        try:
            dom = xml.dom.minidom.parseString(doc)
            impls = dom.documentElement.getElementsByTagName('impl')
            prodClass = _processImpls(impls)
            rss = dom.documentElement.getElementsByTagName('rs')
            press = dom.documentElement.getElementsByTagName('pres')
            rs = None
            pres = None
            if rss:
                rs = _toString(rss[-1])
            elif press:
                pres = press[-1].toxml()
            
            return (prodClass, rs, pres)
        finally:
            if dom != None:
                dom.unlink()
            


    
    def _loadProductFile(self, fname):
        f = None
        
        try:
            f = file(fname)
            doc = f.read()
            return self._parseProductDoc(doc)
        finally:
            if f != None:
                f.close()
            




def _toString(node):
    s = ''
    for child in node.childNodes:
        if child.nodeType == node.CDATA_SECTION_NODE:
            xml = child.toxml()
            cdtag = '<![CDATA['
            p1 = xml.find(cdtag) + len(cdtag)
            p2 = xml.find(']]>')
            s += xml[p1:p2]
        else:
            s += child.toxml()
    
    return s


def _processImpls(impls):
    if len(impls) == 0:
        return Product
    
    impl = impls[-1]
    py = _toString(impl)
    ns = twc.buildPyNamespace()
    exec py in ns, ns
    prodClass = ns['Product']
    return prodClass

