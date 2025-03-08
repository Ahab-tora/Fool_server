import sys
import os
#where are the sequences  -> Element
#what are the sequences ->Element Type
#what are the shots -> components
#what folders are in the shots -> ComponentPart
#what folders are in the ComponentParts ->ComporentPart lower layer

sequences = 'SQ0010','SQ0020','SQ0040' #element type
shots = 'sh0010','sh0020','sh0030' #components




#--- --- --- 

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
    
animTestConfig = {
    'name':'anim',
    'parentElement':None,
    'inPath':'anim',
    'outPath':'scenes',
    'components':[]
}

mayaTestConfig = {
    'name':'maya',
    'parentElement':None,
    'inPath':'maya',
    'outPath':'scenes',
    'components':[animTestConfig]
}

test = Element.fromDict(data=mayaTestConfig)
print(test.components)
for component in test.components:
    print(component.name)
sys.exit()
SequencesFolder = Element(name='SequencesFolder ',inPath='\\\\Storage\\esma\\3D4\\threeLittlePigs\\05_shot')

#---
SQ0010 = Element(name='SQ0010',inPath='SQ0010')
SequencesFolder.addComponent(SQ0010)

#---
sh0010 = Element(name='sh0010',inPath='sh0010')
SQ0010.addComponent(sh0010)

#--- ---
mayaFolder = Element(name='maya',inPath='maya',outPath='scenes')
sh0010.addComponent(mayaFolder)

#---
mayaAnimFolder = Element(name='anim',inPath='anim')
mayaFolder.addComponent(mayaAnimFolder)

#---
mayaAnimEditFolder = Element(name='edit',inPath='edit')
mayaAnimPublishFolder = Element(name='publish',inPath='publish')
mayaAnimFolder.addComponents([mayaAnimEditFolder,mayaAnimPublishFolder])

#--- ---
houdiniFolder = Element(name='houdini',inPath='houdini')
sh0010.addComponent(houdiniFolder)

#--- 
#houdiniFolder.addComponents
houdiniNames = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'
houdiniSubfolders = []
for houdiniName in houdiniNames:
    houdiniSubfolders.append(Element(name=houdiniName,inPath=houdiniName)) 
houdiniFolder.addComponents(houdiniSubfolders)
import pprint
x = houdiniFolder.toDict(lowerHierachy=False,upperHierachy=True)
pprint.pp(x)
'''print(houdiniFolder.components)
print(mayaAnimPublishFolder.fullPath())'''
