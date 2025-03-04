import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import data
#from ...data import global_variables
import datetime
import aiosqlite
import asyncio
from pathlib import Path
from modules.db_interactions.populate_files_db import populate_assets_db,populate_assets_content_db
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
        print(event)
        
        try:
            asset_type,asset_name = self.get_asset_type(path=event.src_path)
            print(asset_type,asset_name)
        except:
            return
        
        if not asset_type:
            return
        else:
            update_database(asset_type=asset_type)

    def get_asset_type(self,path):
        '''
        check if the db needs to be updated , if yes returns 
        '''
        print(f'got signal for {path}')
        path = Path(path)
        if path.is_relative_to(global_variables.assets_path):
            asset_type,asset_name = path.relative_to(global_variables.assets_path).parts[:2]
            return asset_type,asset_name
        
        return None
    

def update_database(asset_type):
    print('updating', asset_type)

    populate_assets_db(scan_path=global_variables.assets_path + '\\' + asset_type,
                       asset_type=asset_type,
                       table_path= global_variables.assets_db_path + '\\' + asset_type +'.db')
    data = populate_assets_content_db(pipeline_path=global_variables.pipeline_path,
                               asset_type=asset_type,
                               table_path= global_variables.assets_db_path  + '\\' + asset_type +'.db')
    #print(data)



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