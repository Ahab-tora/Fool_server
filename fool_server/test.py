

# Sequences
# Sequences Maya template
#from bottom to top
from modules.elements.element import Element
#--- --- --- Sequences config
#--- --- ---Maya config 
#--- 

mayaStatusConfig = []
for status in ['edit','publish']:
    statusConfig = {
        'name':status,
        'parentElement':None,
        'inPath':status,
        'outPath':'',
        'components':[]
    }
    mayaStatusConfig.append(statusConfig)

#---
mayaDepartmentConfig = []
for department in ['anim','layout','render']:
    departmentConfig = {
        'name':department,
        'parentElement':None,
        'inPath':department,
        'outPath':'',
        'components':mayaStatusConfig
    }
    mayaDepartmentConfig.append(departmentConfig)

#---
mayaSQConfig = {
    'name':'maya',
    'parentElement':None,
    'inPath':'maya',
    'outPath':'scenes',
    'components':mayaDepartmentConfig
}

#--- --- --- Houdini config

#--- 
houdiniDepartmentsConfig = []
for department in ['abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video']:
    departmentConfig = {
        'name':status,
        'parentElement':None,
        'inPath':status,
        'outPath':'',
        'components':[]
    }
    houdiniDepartmentsConfig.append(departmentConfig)


#--- 
houdiniSQConfig = {
    'name':'houdini',
    'parentElement':None,
    'inPath':'houdini',
    'outPath':'s',
    'components': houdiniDepartmentsConfig
}



shit

import pprint,os,json
appPath=os.path.dirname(os.path.abspath(__file__))



HoudiniConfig = Element.fromDict(data=mayaSQConfig)


with open(appPath + f'\\data\\config\\{configFileName}.json', "w") as file:
            json.dump(HoudiniConfig.toDict(),file,indent=4)