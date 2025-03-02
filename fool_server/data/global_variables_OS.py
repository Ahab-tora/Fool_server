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
#path to the template that is used to create assets
asset_template_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\04_asset\\template\\_template_workspace_asset'

# --- --- Self paths
server_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
databases_path = server_path + '\\data\\files_db'

# --- --- Pipeline paths
pipeline_path = '\\\\Storage01\\3D4\\orchidSquare'
assets_path = pipeline_path + '\\04_asset'
sequences_path = pipeline_path + '\\06_shot'
team_tools_path = pipeline_path + '\\pipeline\\team_tools'

# --- --- Version
version = '1.0.25022025'

# --- --- Server
host = '10.69.240.231'
port  = 8000
router_prefix = "/OS"

# --- --- Ftrack
api_key = 'YWUwZGY2MGEtYjA4NS00NzcyLThjYzItNTk4NTJkODQ5MWNiOjo2YjZkNjA0Ni00NDZmLTQ4YTctODU3Yy0zNzQ2MDc0M2FmNTk'
project_name = 'END'
project_users = 'Leriche','Chalmet','Kidangan','Maestracci','VANDERWEYEN','Guinet--Elmi','Kumar','Hatef','NGUYEN'
ftrack_server_url = 'https://esma-lyon.ftrackapp.com'
