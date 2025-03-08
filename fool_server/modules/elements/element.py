import os
class Element():
    def __init__(self,name:str = 'Element',inPath:str = '',outPath:str = '',layer:int = 0):
        self.name = name
        self.parentElement = None
        self.inPath = inPath
        self.outPath = outPath
        self.layer = layer
        self.components = []

    def addComponent(self,component):
        component.parentElement = self
        self.components.append(component)

    def addComponents(self,components:list):
        for component in components:
            self.addComponent(component=component)
    
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
        componentsDict = []
        if lowerHierachy and self.components:
            
            for component in self.components:
                componentDict = component.toDict()
                componentsDict.append(componentDict)

        elementDict = {
            'name':self.name,
            'parentElement' :self.parentElement.name if self.parentElement  else None,
            'inPath' : self.inPath ,
            'outPath' : self.outPath ,
            'layer' : self.layer ,
            'components' : componentsDict
            }
        return elementDict

    @classmethod
    def fromDict(cls, data: dict):

        element = cls(
            name =data['name'],
            inPath =data['inPath'],
            outPath =data['outPath'],
            layer =data.get('layer', 0)  )

        for component_data in data.get('components', []):
            component = cls.fromDict(component_data)
            element.addComponent(component)
        return element