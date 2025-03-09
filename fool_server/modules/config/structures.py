import os

class Element():
    def __init__(self,name:str = 'Element',inPath:str = '',outPath:str = '',layer:int = 0):
        self.name = name
        self.parentElement = None
        self.inPath = inPath
        self.outPath = outPath
        self.layer = layer
        self.childrenElements = []

    def addChildElement(self,element):
        element.parentElement = self
        self.childrenElements.append(element)

    def addChildrenElements(self,elements:list):
        for element in elements:
            self.addChildElement(element=element)
    
    def fullPath(self) -> str:
        pathsList = []
        if self.parentElement:
            pathsList.append(self.parentElement.fullPath())

        pathsList.append(self.inPath)
        pathsList.append(self.outPath)

        fullPath = os.path.join(*pathsList)
        return fullPath

    def toDict(self,lowerHierachy:bool = True,upperHierachy:bool = False) -> dict:
        
        if upperHierachy:
            if self.parentElement:
                return self.parentElement.toDict(lowerHierachy=False,upperHierachy=True)
            else:
                return self.toDict(lowerHierachy=True,upperHierachy=False)
            
        childrenElementsDict = []
        if lowerHierachy and self.childrenElements:
            for childElement in self.childrenElements:
                childrenElementsDict.append(childElement.toDict())

        elementDict = {
            'name':self.name,
            'parentElement' :self.parentElement.name if self.parentElement else None,
            'inPath' : self.inPath ,
            'outPath' : self.outPath ,
            'layer' : self.layer ,
            'childrenElements' : childrenElementsDict
            }
        return elementDict

    @classmethod
    def fromDict(cls, data: dict):

        element = cls(
            name =data['name'],
            inPath =data['inPath'],
            outPath =data['outPath'],
            layer =data.get('layer', 0)  )

        for element_data in data.get('childrenElements', []):
            childElement = cls.fromDict(element_data)
            element.addChildElement(childElement)
        return element