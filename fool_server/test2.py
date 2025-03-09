

#iterdir over config files
#create a folder if it does not exist --> ex: files_db/sequences
#check the first layer of elements and create database for each
#fill database with the data using the config file

import sqlite3,json,pprint
from pathlib import Path
import datetime 
from data import global_variables
#need to rename here

with open ('F:\\Fool_server\\fool_server\\data\\config\\shotConfig.json') as file:
    shotConfig = json.load(file)



def createTable(dbCreationPath:str,db_name:str):

    connection = sqlite3.connect(dbCreationPath+'\\'+db_name)
    cursor=connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    query = (f'''
    CREATE TABLE IF NOT EXISTS elementsTable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT ,
    fullPath TEXT NOT NULL UNIQUE,
    inPath TEXT,
    outPath TEXT,
    layer INTEGER DEFAULT 0,
    parentId INTEGER,
    FOREIGN KEY (parentId) REFERENCES elements (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS filesTable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    fullPath TEXT UNIQUE,
    type TEXT,
    size TEXT,
    lastModif TEXT,
    comment TEXT,
    parentId INTEGER,
    FOREIGN KEY (parentId) references elementsTable(id)
    )
    ''')
    cursor.executescript(query)
    connection.commit()
    connection.close()


createTable(dbCreationPath=global_variables.sequences_db_path,db_name='testDb.db')

def getFileData(filePath: str) -> tuple:
    """
    Returns a tuple with file information in this order:
    name, type, path, size, creation_date, last_modification, parent, children
    """
    file = Path(filePath)
    file_stat = file.stat()
    name = file.name.split('\\')[-1]
    type = "folder" if file.is_dir() else file.suffix.lstrip('.') or "unknown"
    path = str(file.resolve())
    size = "0MB" if file.is_dir() else f"{round(file_stat.st_size / (1024 * 1024), 2)}MB"

    
    creation_date = str(datetime.datetime.fromtimestamp(file_stat.st_birthtime))
    last_modification = str(datetime.datetime.fromtimestamp(file_stat.st_mtime))
    #fool_ID = str(uuid.uuid4())
    parent = str(file.parent)

    # Return as a tuple
    return (
        name,
        type,
        path,
        size,
        
        last_modification,
        parent
    )

def getFilesData(filePath:str)->list[tuple]:
    '''
    get the data of all the files in a folder
    '''
    yieldPath = Path(filePath)
    filesData = []
    for file in yieldPath.iterdir():
        filesData.append(getFileData(filePath=file))
    return filesData

#getFilesData(filePath='C:\\Users\\laure\\OneDrive\\Bureau\\05_shit')


#begin with one file path
#C:\Users\laure\OneDrive\Bureau\05_shit
import os

#prendre tous les elemnts(sequence,asset_type) depuis une list(ecrite ou iterdir), avec un path ou les elements sont situés
#regarde ce qu'il y a dedans --> shots,assets
inPath = 'C:\\Users\\laure\\OneDrive\\Bureau\\05_shit\\SQ0010\\SH0010'


def insertElementData(tablePath:str,data:tuple,manageConnection:bool=True,cursor=None):
    if manageConnection:
        connection = sqlite3.connect(tablePath)
        cursor = connection.cursor()

    query = '''
    INSERT OR IGNORE INTO elementsTable(
        name,fullPath, inPath, outPath, layer, parentId)
    VALUES (?,?, ?, ?, ?, ?)
    '''
    cursor.execute(query, data)
    elementId = cursor.lastrowid

    if manageConnection:
        connection.commit()
        connection.close()
    return elementId


def insertFileData(tablePath:str,data:tuple,manageConnection:bool = True,parentId:int = 0,cursor = None):

    if manageConnection is True:
            connection = sqlite3.connect(tablePath)
            cursor=connection.cursor()
    print(data,parentId)
    fullData = data + (parentId,)
    query = '''
    INSERT OR IGNORE INTO filesTable(
    name,fullPath,type,size,lastModif,comment,parentId)
    VALUES (?,?,?,?,?,?,?)
    '''
    cursor.execute(query,fullData)

    if manageConnection is True:
        connection.commit()
        connection.close()


def insertFilesData(tablePath:str,filesData:list[tuple],manageConnection:bool = True,parentId:int = None,cursor = None):

    if manageConnection is True:
            connection = sqlite3.connect(tablePath)
            cursor=connection.cursor()

    fullData = []
    for fileData in filesData:
        fullFileData =fileData + (parentId,)
        print(fullFileData)
        fullData.append(fullFileData)

    query = '''
    INSERT OR IGNORE INTO filesTable(
    name,fullPath,type,size,lastModif,comment,parentId)
    VALUES (?,?,?,?,?,?,?)
    '''
    cursor.executemany(query,fullData)

    if manageConnection is True:
        connection.commit()
        connection.close()



def test(tablePath:str,configs:list,name:str,inPath:str,outPath:str = ''):
    contentPath = os.path.join(inPath,outPath)

    def getFolderStructure(path:str)->dict:
        """ Recursively gets folder structure as a nested dict. """
        structure = {}
        for entry in os.scandir(path):
            if entry.is_dir():
                structure[entry.name] = getFolderStructure(entry.path)
        return structure
    
    folderStructure = getFolderStructure(path=contentPath)


    def compare(config:dict,folderStructure,parentPath=''):

        if config['inPath'] in folderStructure:
            currentStructure = folderStructure[config['inPath']]
            fullPath = os.path.join(parentPath, config['inPath'])

            print(fullPath)
            connection = sqlite3.connect(tablePath)
            cursor=connection.cursor()
            parentId=0
            if parentPath:
                query = '''
                SELECT id FROM elementsTable
                WHERE name = ? AND fullPath = ?
                '''
                
                cursor.execute(query, (name, fullPath))
                parentId = cursor.fetchone()

            elementData = (
            config['name'],  
            fullPath,
            config['inPath'],  
            config['outPath'],  
            config.get('layer', 0), 
            parentId)
            filesData = getFilesData(fullPath)
        
            insertElementData(tablePath=tablePath,data=elementData,manageConnection=False,cursor=cursor)
            insertFilesData(tablePath=tablePath,filesData=filesData,manageConnection=False,cursor=cursor)

            connection.commit()
            connection.close()

            if config['outPath'] and config['outPath'] in currentStructure:
                fullPath = os.path.join(fullPath, config['outPath'])
                
                currentStructure = currentStructure[config['outPath']]

            if config['childrenElements']:
                for childConfig in config['childrenElements']:
                    compare(config=childConfig,folderStructure=currentStructure,parentPath=fullPath)
            
    
    connection = sqlite3.connect(tablePath)
    cursor=connection.cursor()

    for config in configs:
        compare(config=config,folderStructure=folderStructure,parentPath=inPath)
            
           
            #a = getFilesData(fullPath)
            #print(a)   

    connection.commit()
    connection.close()
    
    #pprint.pp(folderStructure)

test(tablePath='F:\\Fool_server\\fool_server\\data\\files_db\\sequences\\testDb.db',name='sh0010',inPath=inPath,configs=shotConfig)

def insertElement(path:str):
    pass
    
def insertFile():
    pass