#--- --- Imports --- ---#
from fastapi import FastAPI,APIRouter
import aiosqlite
from pathlib import Path

import data.global_variables as global_variables
vars_router = APIRouter(prefix="/vars", tags=["vars"])

#--- --- ---

@vars_router.get('/version')
def get_version():
    'returns the current version'
    return global_variables.version

#--- --- ---

@vars_router.get('/get_pipeline_path')
def get_pipeline_path():
    'returns pipeline_path'
    return global_variables.pipeline_path

#--- --- ---

@vars_router.get('/get_assets_path')
def get_assets_path():
    'returns the assets path'
    return global_variables.assets_path

#--- --- ---

@vars_router.get('/get_asset_template_path')
def get_template_path():
    'returns the template_path'
    return global_variables.asset_template_path

#--- --- ---

@vars_router.get('/get_api_key')
def get_api_key():
    'returns the api key of ftrack'
    return global_variables.api_key

#--- --- ---

@vars_router.get('/get_project_name')
def get_project_name():
    'returns the project name'
    return global_variables.project_name

#--- --- ---

@vars_router.get('/get_ftrack_server_url')
def get_ftrack_server_url():
    return global_variables.ftrack_server_url

#--- --- ---

@vars_router.get('/get_project_users')
def get_project_users():
     return global_variables.project_users

#--- --- ---

@vars_router.get('/get_assets_types')
def get_assets_types():
    return global_variables.assets_types

#--- --- ---

@vars_router.get('/get_team_tools_path')
def get_team_tools_path():
    return global_variables.team_tools_path