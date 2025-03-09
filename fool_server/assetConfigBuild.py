
from modules.config.structures import Element


mayaStatusConfigs = []
for status in ['edit','publish']:
    mayaStatusConfig = {
        'name':status,
        'parentElement':None,
        'inPath':status,
        'outPath':'',
        'childrenElements':[]
    }
    mayaStatusConfigs.append(mayaStatusConfig)

#---
mayaDepartmentConfigs = []
for department in ['assetLayout','cloth','dressing','groom','lookdev','modeling','rig','sculpt']:

    mayaDepartmentConfig = {
        'name':department,
        'parentElement':None,
        'inPath':department,
        'outPath':'',
        'childrenElements':mayaStatusConfigs
    }
    mayaDepartmentConfigs.append(mayaDepartmentConfig)

#---
mayaSQConfig = {
    'name':'maya',
    'parentElement':None,
    'inPath':'maya',
    'outPath':'scenes',
    'childrenElements':mayaDepartmentConfigs
}

#--- --- --- Houdini config

#--- 
houdiniDepartmentsConfig = []
for department in ['abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video']:
    departmentConfig = {
        'name':department,
        'parentElement':None,
        'inPath':department,
        'outPath':'',
        'childrenElements':[]
    }
    houdiniDepartmentsConfig.append(departmentConfig)


#--- 
houdiniSQConfig = {
    'name':'houdini',
    'parentElement':None,
    'inPath':'houdini',
    'outPath':'',
    'childrenElements': houdiniDepartmentsConfig
}
#--- --- ---

#--- --- ---


import pprint,os,json
appPath=os.path.dirname(os.path.abspath(__file__))


mayaConfig = Element.fromDict(data=mayaSQConfig)
houdiniConfig = Element.fromDict(data=houdiniSQConfig)
AssetConfig = [mayaConfig.toDict(),houdiniConfig.toDict()]
configFileName = 'assetConfig'


with open(appPath + f'\\data\\config\\{configFileName}.json', "w") as file:
            json.dump(AssetConfig,file,indent=4)