#--- --- Imports --- ---#
from fastapi import FastAPI,APIRouter
import uvicorn
import sqlite3
import datetime
import os,sys
import aiosqlite
from pathlib import Path
import threading


from modules.db_interactions.populate_files_db import populate_assets_db,populate_assets_content_db
#from modules.db_interactions.assets_updates import watchdog
from modules.db_interactions.assets_updates_2 import watchdog
import data.global_variables as global_variables


for asset_type_path in Path(global_variables.assets_path).iterdir():

    asset_type_name = str(asset_type_path).split('\\')[-1]
    table_path = global_variables.databases_path +'\\'+asset_type_name+'.db'

    populate_assets_db(scan_path=global_variables.assets_path+'\\'+asset_type_name,
                       asset_type=asset_type_name ,
                       table_path=table_path)
    populate_assets_content_db(pipeline_path=global_variables.pipeline_path,
                               asset_type=asset_type_name,
                               table_path=table_path)


watchdog_thread = threading.Thread(target=watchdog, args=(Path(global_variables.assets_path),), daemon=True)
watchdog_thread.start()

host = '127.0.0.1'
port = 8000

#databases_path = 'D:\code\Fool_v3_versions\Fool_v3_15.01.25\fool_server\data\END_data\files_db'
databases_path = os.getcwd() + '\\data\\files_db'
app = FastAPI()
'''python -m uvicorn test:app --reload'''

project_router = APIRouter()

@app.get("/")
def root():
    return {"message": f"Launched at {datetime.datetime.now()}"}

@project_router.get('/get_assets_path')
def get_assets_path():
     return global_variables.assets_path

@project_router.get('/get_pipeline_path')
def get_pipeline_path():
     return global_variables.pipeline_path
     

@project_router.get('/get_assets_types')
def get_assets_types():
    assets_types = []
    for asset_type_path in Path(global_variables.assets_path).iterdir():
        asset_type_name = str(asset_type_path).split('\\')[-1]
        assets_types.append(asset_type_name)
    
    return assets_types

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
    asset_id = asset_row[0]

    files_query = (f'''SELECT name 
                       FROM {asset_type}_data_table 
                       WHERE department IS ?
                       AND parent_id IS ?
                       AND status IS ?
                      ''')
        
    await cursor.execute(files_query,(department,asset_id,status))

    results = await cursor.fetchall()
    results_formatted = list(reversed(results))

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

    files_query = (f'''SELECT name 
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


@project_router.post('/set_for_review/{asset_type}/{file}')
async def set_for_review(asset_type:str,file:str):

    connection = await aiosqlite.connect(databases_path + '\\' + asset_type + '.db')
    cursor= await connection.cursor()

    asset_query = (f'''
        SELECT name,path,department
        FROM {asset_type}_data_table
        WHERE name == ?
        ''')
    
    await cursor.execute(asset_query,(file,))
    asset_data= await cursor.fetchone()
 
    await connection.close()

    #--- --- ---

    connection = await aiosqlite.connect(databases_path + '\\publish.db')
    cursor = await connection.cursor()

    insert_query = (f'''
        INSERT OR REPLACE INTO publish_table
        (name, path,department)
        VALUES (?,?,?)
        ''')
    await cursor.execute(insert_query,asset_data)

    await connection.commit()
    await connection.close()


@project_router.get('/get_extension')
async def get_extension(name:str):

    connection = await aiosqlite.connect(databases_path + '\\publish.db')
    cursor = await connection.cursor()

    path_query = ('''
            SELECT path
            FROM publish_table
            WHERE name = ?
            ''')
    await cursor.execute(path_query,(name,))
    file_row = await cursor.fetchall() #returns a table and we only need the first element, that's why we add [0][0] at the end
    file_path = str(file_row[0][0])

    await connection.close()

    return file_path


@project_router.get('/refresh_publish_view')
async def refresh_publish_view():
        connection = await aiosqlite.connect(databases_path + '\\' + 'publish.db')
        cursor = await connection.cursor()

        query = ('''
        SELECT name 
        FROM publish_table
        ''')

        await cursor.execute(query)

        results = await cursor.fetchall()
        await connection.close()
        return results


@project_router.delete('/delete_selection_from_publish/{selection}')
async def delete_selection_from_publish(selection:str):
        '''
        Delete the selection from the publish table
        '''
        connection = await aiosqlite.connect(databases_path + '\\' + 'publish.db')
        cursor = await connection.cursor()

        query = ('''
        DELETE
        FROM publish_table
        WHERE name = ?
        ''')
        await cursor.execute(query,(selection,))
        
        await connection.commit()
        await connection.close()



app.include_router(project_router, prefix=global_variables.router_prefix)
        
uvicorn.run(app, host=global_variables.host, port=global_variables.port)
