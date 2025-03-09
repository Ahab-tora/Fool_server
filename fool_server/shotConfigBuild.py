

# Sequences
# Sequences Maya template
#from bottom to top
from modules.config.structures import Element
#--- --- --- Sequences config
#--- --- ---Maya config 
#--- 

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
for department in ['anim','layout','render']:

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
shotConfig = [mayaConfig.toDict(),houdiniConfig.toDict()]
configFileName = 'shotConfig'


with open(appPath + f'\\data\\config\\{configFileName}.json', "w") as file:
            json.dump(shotConfig,file,indent=4)