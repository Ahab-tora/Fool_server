from watchfiles import watch
from data import global_variables
import aiosqlite,sqlite3
import asyncio,os
from watchfiles import awatch
from test2 import getFilesData,insertFilesData


async def updatesWatcher(queue,path:str):
    async for changes in awatch(path):
        for event,file_path in changes:
            if not os.path.isdir(file_path):
                continue
            print(f"Change detected on {file_path}")
            await queue.put(file_path)

def updateDb(modificationPath:str,dbPath:str,manageConnection:bool,cursor:None):
    '''updates the databse for a given database and path'''
    if manageConnection:
        connection = sqlite3.connect(dbPath)
        cursor = connection.cursor()

    query = '''SELECT id FROM elementsTable WHERE fullPath = ?'''
    cursor.execute(query, (modificationPath,))
    result = cursor.fetchone()

    if result:
        parentId = result[0]
    else:
        if manageConnection:
            cursor.close()
        return

    filesData = getFilesData(folderPath=modificationPath)
    insertFilesData(dbPath=dbPath,filesData=filesData,parentId=parentId,manageConnection=False,cursor=cursor)
    print(f'inserted {filesData}')

    if manageConnection:
        connection.commit()
        cursor.close()


async def test(queue,path:str):
    while True:
        modificationPath = await queue.get()
        if modificationPath is None:
            break
        
        #--- treatment of the path

        dbName = modificationPath.replace(path,'').split('\\')[1]
        dbPath = os.path.join(global_variables.databasesPath,dbName+'.db')

        updateDb(modificationPath=modificationPath,dbPath=dbPath,manageConnection=True,cursor=None)


async def main(path:str):
    queue = asyncio.Queue()
    await asyncio.gather(updatesWatcher(queue=queue,path=path), test(queue=queue,path=path))


asyncio.run(main('C:\\Users\\laure\\OneDrive\\Bureau\\05_shit'))  



