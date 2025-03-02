# --- --- Imports
import os
import sys

# --- --- WARNING --- --- #
'''
Use double \ everywhere BUT if it's a path to a remote server use quadruple slashes
example: '\\\\Storage\\movieName'
'''

# --- --- Config
#names of the folders that are your asset types
assets_types = 'character','item','prop','set'
sequences = ['SQ0010','SQ0020','SQ0030','SQ0040','SQ0050','SQ0060','SQ0070','SQ0080','SQ0090','SQ0100','SQ0100','SQ0120','SQ0130','SQ0010','SQ0140']
#path to the template that is used to create assets
asset_template_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\04_asset\\template\\_template_workspace_asset'
shot_template_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\05_shot\\_template_workspace_shot'

# --- --- Self paths
server_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
databases_path = server_path + '\\data\\files_db'
assets_path = server_path + '\\data\\files_db\\assets'
sequences_db_path = server_path + '\\data\\files_db\\sequences'

# --- --- Pipeline paths
pipeline_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs'
assets_path = pipeline_path + '\\04_asset'
sequences_path = pipeline_path + '\\05_shot'
team_tools_path = pipeline_path + '\\pipeline\\team_tools'

# --- --- Config
#--- Assets
#assets_maya_departments =
assets_status_list = 'edit','publish'
assets_houdini_departments = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

#--- Sequences
sequences_maya_departments ='anim','layout','render'
sequences_status_list = 'edit','publish'
sequences_houdini_departments = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

# --- --- Version
version = '1.0.25022025'

# --- --- Server
host = '10.69.240.231'
port  = 8000
router_prefix = "/END"

# --- --- Ftrack
api_key = 'YWUwZGY2MGEtYjA4NS00NzcyLThjYzItNTk4NTJkODQ5MWNiOjo2YjZkNjA0Ni00NDZmLTQ4YTctODU3Yy0zNzQ2MDc0M2FmNTk'
project_name = 'END'
project_users = 'Leriche','Chalmet','Kidangan','Maestracci','VANDERWEYEN','Guinet--Elmi','Kumar','Hatef','NGUYEN'
ftrack_server_url = 'https://esma-lyon.ftrackapp.com'
