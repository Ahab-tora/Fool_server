# --- --- Imports
import os
import sys

# --- --- WARNING --- --- #
"""
Use double \ everywhere BUT if it's a path to a remote server use quadruple slashes
example: '\\\\Storage\\movieName'
"""

# --- --- Config
'''
dict containing each elements types and data 
path -> where the data is queried
types -> databases names and the 'first layer' inside the path
templatePath -> template of what is contained insied the types
'''
elementData ={
    'sequences':{
                'path':'',
                'types':['SQ0010','SQ0020'],
                'templatePath': '\\\\Storage\\esma\\3D4\\threeLittlePigs\\05_shot\\_template_workspace_shot'

    },
    'assets':{
            'path':'',
            'types':['character','item','prop','set'],
            'templatePath': '\\\\Storage\\esma\\3D4\\threeLittlePigs\\04_asset\\template\\_template_workspace_asset'
    }

}

#--- assets
assets_types = 'character','item','prop','set'
asset_template_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\04_asset\\template\\_template_workspace_asset'

#--- sequences
sequences = 'SQ0010','SQ0020','SQ0030','SQ0040','SQ0050','SQ0060','SQ0070','SQ0080','SQ0090','SQ0100','SQ0120','SQ0130','SQ0010','SQ0140'
shot_template_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\05_shot\\_template_workspace_shot'


# --- --- Self paths
server_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
serverPath =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
databases_path = server_path + '\\data\\files_db'
databasesPath = server_path + '\\data\\files_db'
assets_db_path = server_path + '\\data\\files_db\\assets'
sequences_db_path = server_path + '\\data\\files_db\\sequences'
sequencesDbPath = server_path + '\\data\\files_db\\sequences'

testPath = 'C:\\Users\\laure\\OneDrive\\Bureau\\05_shit'
configsPath = serverPath + '\\data\\config'

# --- --- Pipeline paths
pipeline_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs'
assets_path = pipeline_path + '\\04_asset'
sequences_path = pipeline_path + '\\05_shot'
sequencesPath = pipeline_path + '\\05_shot'
team_tools_path = pipeline_path + '\\pipeline\\team_tools'


# --- --- Config old
#--- Assets
assets_maya_departments = 'assetLayout','cloth','dressing','groom','lookdev','modeling','rig','sculpt'
assets_status = 'edit','publish'
assets_houdini_departments = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

#--- Sequences
sequences_maya_departments ='anim','layout','render'
sequences_status = 'edit','publish'
sequences_houdini_departments = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

# --- --- Version
version = '1.0.20253005'

# --- --- Server
host = '192.168.56.1'
port  = 8000
router_prefix = "/END"

# --- --- Ftrack
api_key = 'YWUwZGY2MGEtYjA4NS00NzcyLThjYzItNTk4NTJkODQ5MWNiOjo2YjZkNjA0Ni00NDZmLTQ4YTctODU3Yy0zNzQ2MDc0M2FmNTk'
project_name = 'END'
project_users = 'Leriche','Chalmet','Kidangan','Maestracci','VANDERWEYEN','Guinet--Elmi','Kumar','Hatef','NGUYEN'
ftrack_server_url = 'https://esma-lyon.ftrackapp.com'
