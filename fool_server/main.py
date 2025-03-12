#--- --- Imports --- ---#
from fastapi import FastAPI,APIRouter
import uvicorn
import datetime
import os
import aiosqlite
from pathlib import Path
import threading

from api.sequences import sequences_router
from modules.db_interactions.populate_files_db import populate_assets_db,populate_assets_content_db
from modules.db_interactions.assets_updates_2 import watchdog
import data.global_variables as global_variables

host = global_variables.host
port = global_variables.port


databases_path = global_variables.assets_db_path

for asset_type in global_variables.assets_types:
    asset_type_path = global_variables.assets_path + '\\' + asset_type

    asset_type_name = str(asset_type_path).split('\\')[-1]
    table_path = global_variables.assets_db_path +'\\'+asset_type_name+'.db'

    populate_assets_db(scan_path=global_variables.assets_path+'\\'+asset_type_name,
                       asset_type=asset_type_name ,
                       table_path=table_path)
    populate_assets_content_db(pipeline_path=global_variables.pipeline_path,
                               asset_type=asset_type_name ,
                               table_path=table_path)

watchdog_thread = threading.Thread(target=watchdog, args=(Path(global_variables.assets_path),), daemon=True)
watchdog_thread.start()




app = FastAPI()
'''python -m uvicorn test:app --reload'''

project_router = APIRouter(prefix=global_variables.router_prefix)

@project_router.get("/ping")
def root():
    'ping to do testing'
    return f"Ping at {datetime.datetime.now()}!"

@project_router.get('/version')
def get_version():
    'returns the current version'
    return global_variables.version

@project_router.get('/get_pipeline_path')
def get_pipeline_path():
    'returns pipeline_path'
    return global_variables.pipeline_path

@project_router.get('/get_assets_path')
def get_assets_path():
    'returns the assets path'
    return global_variables.assets_path

@project_router.get('/get_asset_template_path')
def get_template_path():
    'returns the template_path'
    return global_variables.asset_template_path

@project_router.get('/get_api_key')
def get_api_key():
    'returns the api key of ftrack'
    return global_variables.api_key

@project_router.get('/get_project_name')
def get_project_name():
    'returns the project name'
    return global_variables.project_name

@project_router.get('/get_ftrack_server_url')
def get_ftrack_server_url():
    return global_variables.ftrack_server_url

@project_router.get('/get_project_users')
def get_project_users():
     return global_variables.project_users

@project_router.get('/get_assets_types')
def get_assets_types():
    return global_variables.assets_types

@project_router.get('/get_team_tools_path')
def get_team_tools_path():
    return global_variables.team_tools_path


@project_router.get("/get_assets/{asset_type}")
async def get_assets(asset_type:str):
    '''
    returns assets of a given type for asset_type_asset_table
    '''
    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor = await connection.cursor()
            
    await cursor.execute(f'''SELECT name FROM {asset_type}_asset_table''')
    results = await cursor.fetchall()
    await connection.close()
    
    return results


@project_router.get('/get_assets_from_search/{asset_type}/{search}')
async def get_assets_from_search(asset_type:str,search:str):
    '''
    returns assets of a given type and search for asset_type_asset_table
    '''

    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor= await connection.cursor()

    query = (f'''SELECT name FROM {asset_type}_asset_table WHERE name LIKE ?''')
    await cursor.execute(query, (f"%{search}%",))

    results = await cursor.fetchall()
    await connection.close()

    return results


@project_router.get('/get_files_of_asset/{asset_type}/{asset_name}/{department}/{status}')
async def get_files_of_assset(asset_type:str,asset_name:str,department:str,status:str):
    '''
    returns the files of an asset department and status
    '''
    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor= await connection.cursor()

    asset_id_query = (f'''SELECT asset_id 
                          FROM {asset_type}_asset_table 
                          WHERE name = ? ''')

    await cursor.execute(asset_id_query,(asset_name,))
    asset_row = await cursor.fetchone()
    if not asset_row:
        return None
    asset_id = asset_row[0]

    files_query = (f'''SELECT name,last_modification,comment 
                       FROM {asset_type}_data_table 
                       WHERE department IS ?
                       AND parent_id IS ?
                       AND status IS ?
                      ''')
        
    await cursor.execute(files_query,(department,asset_id,status))

    results = await cursor.fetchall()

    results_formatted = list(reversed(sorted(results,key =lambda x: x[1])))
    await connection.close()

    return results_formatted 


@project_router.get('/get_files_of_asset_search/{asset_type}/{asset_name}/{department}/{status}/{search}')
async def get_files_of_asset_search(search:str,asset_type:str,asset_name:str,department:str,status:str):

    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor= await connection.cursor()


    asset_id_query = (f'''SELECT asset_id 
                          FROM {asset_type}_asset_table 
                          WHERE name = ? ''')

    await cursor.execute(asset_id_query,(asset_name,))
    asset_row = await cursor.fetchone()
    asset_id = asset_row[0]

    files_query = (f'''SELECT name,last_modification,comment  
                       FROM {asset_type}_data_table 
                       WHERE department IS ?
                       AND parent_id IS ?
                       AND status IS ?
                       AND name LIKE ?
                      ''')
        
    await cursor.execute(files_query,(department,asset_id,status,search))

    results = await cursor.fetchall()
    results_formatted = list(reversed(results))
    await connection.close()

    return results_formatted


@project_router.get("/get_file_path_for_reference_drop/{asset_type}/{file}")
async def get_file_path_for_reference_drop(asset_type:str,file:str):

    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor= await connection.cursor()

    query = (f'''SELECT path 
                        FROM {asset_type}_data_table 
                        WHERE name = ? ''')
    await cursor.execute(query,(file,))
    file_row = await cursor.fetchone()
    file_path = file_row[0]
    await connection.close()
    
    return file_path


@project_router.get('/get_path_of_file/{asset_type}/{file}')
async def get_path_of_file(asset_type:str,file:str):

    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor=await connection.cursor()

    query = (f'''SELECT path 
                       FROM {asset_type}_data_table 
                       WHERE name = ? ''')
    await cursor.execute(query,(file,))
    file_row = await cursor.fetchone()
    file_path = file_row[0]

    await connection.close()
    
    return file_path




project_router.include_router(sequences_router)
app.include_router(project_router)
        
uvicorn.run(app, host=global_variables.host, port=global_variables.port)
