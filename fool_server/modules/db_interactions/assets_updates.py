import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import data
#from ...data import global_variables
import datetime
import aiosqlite
import asyncio
from pathlib import Path

import data.global_variables as global_variables

class MyHandler(FileSystemEventHandler):

    def __init__(self):
        print('Launching handler')
        self.last_called = 0


    def on_any_event(self, event):
        #when a change happens on the pipe, add the new files to the treemodel
        #this function has a filter to not fully execute it more than once every second to avoid lags and visual problems
        call = time.time()
        time_passed = call - self.last_called

        #time filter to avoid having more than 1 call/second
        if time_passed  <= 1:
            self.last_called = call
            return
        self.last_called = call

        try:
            asset_type,asset_name = self.get_asset_type(path=event.src_path)
        except:
            return
        
        if not asset_type:
            return
        else:
            asyncio.run(handle_event(asset_type=asset_type,asset_name=asset_name,asset_path=global_variables.assets_path+'\\'+asset_type+'\\'+asset_name))


    def get_asset_type(self,path):
        '''
        check if the db needs to be updated , if yes returns 
        '''
        print(f'got signal for {path}')
        path =Path(path)
        if path.is_relative_to(global_variables.assets_path):
            asset_type,asset_name = path.relative_to(global_variables.assets_path).parts[:2]
            return asset_type,asset_name
        
        return None
    

async def handle_event(asset_name,asset_type,asset_path):

    async def insert_data(entry, department, status, parent_id):
        """
        Insert or update entry into the db
        """
        name = entry.name
        path = str(entry)
        file_type = entry.suffix.lstrip('.') or "unknown"
        last_modification = str(datetime.datetime.fromtimestamp(entry.stat().st_mtime))
            
        await cursor.execute(f'''
        INSERT INTO {asset_type}_data_table (
        name, path, type, department, status, parent_id, last_modification
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
        last_modification=excluded.last_modification;
         ''', (name, path, file_type, department, status, parent_id, last_modification))

    connection = await aiosqlite.connect(global_variables.databases_path + '\\' + asset_type + '.db')
    cursor = await connection.cursor()
    

    data = (asset_name,str(asset_path),asset_type)

    await cursor.execute(f'''
        INSERT OR IGNORE INTO '{asset_type}_asset_table'
        (name,path,type)
        VALUES (?, ?, ?)
        ''', data)

    await  cursor.execute(f'''SELECT asset_id FROM {asset_type}_asset_table WHERE name = ?''', (asset_name,))
    results = await cursor.fetchone()
    
    try:
        parent_id = results[0]
    except:
        return
    
    await connection.close()

    maya_departments = ['assetLayout', 'cloth', 'dressing', 'groom', 'lookdev', 'modeling', 'rig']
    status_list = ['edit', 'publish']
    for status in status_list:
        for department in maya_departments:
            maya_path = Path(global_variables.assets_path + '\\' + asset_name +  '\\maya\\scenes\\' + status + '\\' + department)
            if maya_path.exists():
                for entry in maya_path.iterdir():
                    if entry.is_file():
                        insert_data(entry, department, status, parent_id)

    # Process files in Houdini departments
    houdini_departments = ['abc', 'audio', 'comp', 'desk', 'flip', 'geo', 'hdz', 'render', 'scripts', 'sim', 'tex', 'video']
    for department in houdini_departments:
        houdini_path = Path(global_variables.assets_path + '\\' + asset_name + '\\' + 'houdini\\' + department) 
        if houdini_path.exists():
            for entry in houdini_path.iterdir():
                if entry.is_file():
                    insert_data(entry, department, "None", parent_id)

    await connection.commit()
    await connection.close()
    



def watchdog(pipeline_path):
    print('Launching watchdog')
    event_handler = MyHandler()
    observer = Observer()       
    print_count = 0 
    observer.schedule(event_handler,pipeline_path, recursive=True)  
    observer.start() 

    try:
        while True:
            time.sleep(2)  
            print_count +=1
            if print_count % 100 == 0 :
                print(f'watchdog still watchdogging,executed {print_count} times')

    except KeyboardInterrupt:
        observer.stop() 
    observer.join()      

#watchdog(pipeline_path=global_variables.assets_path)