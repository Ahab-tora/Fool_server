#--- --- Imports --- ---#
from fastapi import FastAPI,APIRouter
import aiosqlite,pprint,json,os
from pathlib import Path

import data.global_variables as global_variables


#--- --- ---

#--- --- ---
queryRouter = APIRouter(prefix='/query')

@queryRouter.get('/getElements')
async def getElements()->list:
    'returns the elements'
    return list(global_variables).elementData.keys()

#--- ---

@queryRouter.get('/getTypes/{element}')
async def getTypes(element:str)->list:
    'returns the types of an element'
    return global_variables.elementData[element]['types']

#--- ---

@queryRouter.get('/getConfig/{element}')
async def getConfig(element:str):
    try:
        configName = element + 'Config.json'
        print(configName)
        configPath = os.path.join(global_variables.configsPath , configName)
        print(configPath)
        with open(configPath,'r') as file:
            configDict = json.load(file)
        return configDict
    except:
        return {}

#--- ---

@queryRouter.get("/getFiles/{dbName}")
async def getFiles(dbName:str,parentPath:str)->list:
    '''returns the data of the files for a given database and element path'''
    print(dbName,parentPath)
    connection = await aiosqlite.connect(global_variables.databasesPath + '\\' + dbName + '.db')
    cursor = await connection.cursor()

    #---
    query = '''
    SELECT id 
    FROM elementsTable
    WHERE fullPath = ?
    '''
    await cursor.execute(query,(parentPath,))
    parentId = await cursor.fetchone()
    if not parentId:
        await connection.close()
        return []

    #--- 
    query = '''
    SELECT name,fullPath,type,size,lastModif,comment 
    FROM filesTable
    WHERE parentId = ?
    '''
    await cursor.execute(query,parentId)
    filesData = await cursor.fetchall()

    pprint.pp(filesData)
    await connection.close()
    return filesData

#--- ---

@queryRouter.get('/getRoots/{dbName}')
async def getRoots(dbName:str)->list:
    '''returns the elements without parents , the roots'''
    connection = await aiosqlite.connect(global_variables.databasesPath + '\\' + dbName + '.db')
    cursor = await connection.cursor()
    #---
    query = '''
    SELECT name 
    FROM elementsTable
    WHERE parentId is NULL
    '''
    await cursor.execute(query)
    roots = await cursor.fetchall()
    if not roots:
        await connection.close()
        return []
    rootsList = []
    for rootTuple in roots:
        rootsList.append(rootTuple[0])
    await connection.close()
    return rootsList

#--- ---

@queryRouter.get('/getChildren')
async def getChildren(dbName:str):
    connection = await aiosqlite.connect(global_variables.databasesPath + '\\' + dbName + '.db')
    cursor = await connection.cursor()

    await connection.close()
