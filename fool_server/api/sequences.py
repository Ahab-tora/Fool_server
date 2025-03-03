#--- --- Imports --- ---#
from fastapi import FastAPI,APIRouter
import aiosqlite
from pathlib import Path

import data.global_variables as global_variables
sequences_router = APIRouter(prefix="/sequences", tags=["Sequences"])

databases_path = global_variables.sequences_db_path

@sequences_router.get("/ping")
def root():
    'ping to do testing'
    return "Ping!"

'''
get sequences
get shots	/sequence ok
get files of shot	/sequence/shot/status/department
get file path for ref drop	/sequence/shot/status/department ???
get path of file	/sequence/shot/status/department ???
'''

@sequences_router.get('/get_sequences')
def get_sequences():
    return global_variables.sequences

@sequences_router.get('/get_sequences_maya_departments')
def get_sequences_maya_departments():
    return global_variables.sequences_maya_departments

@sequences_router.get('/get_sequences_status')
def get_sequences_status():
    return global_variables.sequences_status

@sequences_router.get('/get_sequences_houdini_departments')
def get_sequences_houdini_departments():
    return global_variables.sequences_houdini_departments

@sequences_router.get('/get_shots_template_path')
def get_shots_template_path():
    return global_variables.shot_template_path


@sequences_router.get('/get_shots/{sequence}')
async def get_shots(sequence):
    '''returns the shots of a given sequence'''

    connection = await aiosqlite.connect(databases_path + '\\' + sequence + '.db')
    cursor = await connection.cursor()

    await cursor.execute(f'''SELECT name FROM {sequence}_shots_table''')
    results = await cursor.fetchall()
    await connection.close()
    shots = []
    for shot in results:
        shots.append(shot[0])
    return shots

@sequences_router.get('/get_files/{sequence}/{shot}/{status}/{department}')
async def get_files(sequence:str,shot:str,status:str,department:str):
    '''
    returns the files of an a shot status and department
    '''
    connection = await aiosqlite.connect(databases_path + '\\' + sequence + '.db')
    cursor= await connection.cursor()

    shot_id_query = (f'''SELECT shot_id 
                          FROM {sequence}_shots_table 
                          WHERE name = ? ''')

    await cursor.execute(shot_id_query,(shot,))
    shot_row = await cursor.fetchone()
    shot_id = shot_row

    files_query = (f'''SELECT name,last_modification,comment 
                       FROM {sequence}_data_table 
                       WHERE department IS ?
                       AND parent_id IS ?
                       AND status IS ?
                      ''')
        
    await cursor.execute(files_query,(department,shot_id,status))

    results = await cursor.fetchall()

    results_formatted = list(reversed(sorted(results,key =lambda x: x[1])))
    await connection.close()
    
    return results_formatted 

@sequences_router.get("/get_shot_path/{sequence}/{shot}")
async def get_shot_path(sequence:str,shot:str): 

    connection = await aiosqlite.connect(databases_path + '\\' + sequence + '.db')
    cursor= await connection.cursor()

    query = (f'''SELECT path 
                        FROM {sequence}_shots_table 
                        WHERE name = ? ''')
    await cursor.execute(query,(shot,))
    file_row = await cursor.fetchone()
    file_path = file_row[0]
    await connection.close()
    
    return file_path