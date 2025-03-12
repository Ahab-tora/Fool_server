

#iterdir over config files
#create a folder if it does not exist --> ex: files_db/sequences
#check the first layer of elements and create database for each
#fill database with the data using the config file
78
import sqlite3,json,pprint,os,aiosqlite,asyncio
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




def getFileData(filePath: str) -> tuple:
    """
    Returns a tuple with file information in this order:
    name, path,type, size, last_modification
    """
    file = Path(filePath)
    file_stat = file.stat()
    name = file.name.split('\\')[-1]
    type = 'Folder' if file.is_dir() else file.suffix.lstrip('.') or "unknown"
    path = str(file.resolve())
    size = '' if file.is_dir() else f"{round(file_stat.st_size / (1024 * 1024), 2)}MB"

    
    #creation_date = str(datetime.datetime.fromtimestamp(file_stat.st_birthtime))
    last_modification = str(datetime.datetime.fromtimestamp(file_stat.st_mtime))
    #fool_ID = str(uuid.uuid4())
    #parent = str(file.parent)

    # Return as a tuple
    return (
        name,
        path,
        type,
        size,
        last_modification,
    )

#--- ---

def getFilesData(filePath:str)->list[tuple]:
    '''
    get the data of all the files in a folder
    '''
    yieldPath = Path(filePath)
    filesData = []
    for file in yieldPath.iterdir():
        filesData.append(getFileData(filePath=file))
    return filesData

#--- ---

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

#--- ---

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

#--- ---

def insertFilesData(tablePath:str,filesData:list[tuple],manageConnection:bool = True,parentId:int = None,cursor = None):

    if manageConnection is True:
            connection = sqlite3.connect(tablePath)
            cursor=connection.cursor()

    fullData = []
    for fileData in filesData:
        print(parentId)
        fullFileData = fileData + (parentId,)
        fullData.append(fullFileData)

    query = '''
    INSERT OR IGNORE INTO filesTable(
    name,fullPath,type,size,lastModif,parentId)
    VALUES (?,?,?,?,?,?)
    '''
    cursor.executemany(query,fullData)

    if manageConnection is True:
        connection.commit()
        connection.close()

#--- ---

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


    def compare(cursor,config:dict,folderStructure,parentPath=''):

        if config['inPath'] in folderStructure:
            currentStructure = folderStructure[config['inPath']]
            
            fullPath = os.path.join(parentPath, config['inPath'])
            if not fullPath.endswith(config['outPath']):
                print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                fullPath = os.path.join(parentPath, config['inPath'],config['outPath'])

            parentId=0

            if parentPath:
                query = '''SELECT id FROM elementsTable WHERE fullPath = ?'''
                cursor.execute(query, (str(parentPath),))
                result = cursor.fetchone()
                if result:
                    parentId = result[0]
                else:
                    parentId = None

            print('--- --- ---')
            print(fullPath)
            print(parentPath)
            print(parentId)
            print('--- --- ---')
            elementData = (
            config['name'],  
            fullPath,
            config['inPath'],  
            config['outPath'],  
            config.get('layer', 0), 
            parentId)

            filesData = getFilesData(fullPath)
        
            parentId = insertElementData(tablePath=tablePath,data=elementData,manageConnection=False,cursor=cursor)
            insertFilesData(tablePath=tablePath,filesData=filesData,parentId=parentId,manageConnection=False,cursor=cursor)
            
            connection.commit()
            

            if config['outPath'] and config['outPath'] in currentStructure:
                fullPath = os.path.join(parentPath, config['inPath'])
                if not fullPath.endswith(config['outPath']):
                    fullPath = os.path.join(fullPath, config['outPath'])
                            
                currentStructure = currentStructure[config['outPath']]

            if config['childrenElements']:
                for childConfig in config['childrenElements']:
                    compare(cursor=cursor,config=childConfig,folderStructure=currentStructure,parentPath=fullPath)
            
    connection = sqlite3.connect(tablePath)
    cursor=connection.cursor()        
    
    #root (shor or asset)
    elementDataRoot = (
        name,  
        str(inPath),
        '',  
        outPath,  
        0, 
        None)
    insertElementData(tablePath=tablePath,data=elementDataRoot,cursor=cursor)
    for config in configs:
        compare(config=config,folderStructure=folderStructure,parentPath=inPath,cursor=cursor)
    connection.close()
           

global_variables.databasesPath
createTable(dbCreationPath=global_variables.sequences_db_path,db_name='testDb.db')

sequencesPath = Path('C:\\Users\\laure\\OneDrive\\Bureau\\05_shit\\SQ0010')
for sequence in  global_variables.sequences:

    sequencePath = Path(sequencesPath + sequence)
    dbName = sequence + '.db'
    dbPath = global_variables.databases_path + dbName
    if os.path.exists()  :
    
            createTable(dbCreationPath=global_variables.sequences_db_path,db_name='testDb.db')

    for shotPath in sequencePath.iterdir():

        shotName = str(shotPath).split('\\')[-1]
        test(tablePath='F:\\Fool_server\\fool_server\\data\\files_db\\sequences\\testDb.db',name=shotName,inPath=shotPath,configs=shotConfig)

tb = 'F:\\Fool_server\\fool_server\\data\\files_db\\sequences\\testDb.db'

async def getRoots(tablePath,manageConnection:bool,cursor = None)->list[str]:
    if manageConnection:
        connection = await aiosqlite.connect(tablePath)
        cursor = await connection.cursor()

    query = '''SELECT name 
            FROM elementsTable
            WHERE parentId IS NULL'''

    await cursor.execute(query)
    roots = await cursor.fetchall()
    print(roots)

    for i,element in enumerate(roots):
        roots[i] = roots[i][0]
    print(roots)

    if manageConnection:
        await cursor.close()

    return roots


