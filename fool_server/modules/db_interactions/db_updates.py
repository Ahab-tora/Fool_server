import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



import END_data

from populate_files_db import *



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

        asset_types = 'character','item','prop','set'
        
        for asset_type in asset_types:
            asset_type_path = END_data.pipeline_path + '\\04_asset' + '\\' + asset_type
            print(event.src_path)
            if asset_type_path in event.src_path:
                print('True')

                populate_assets_db(scan_path=pipeline_path+item_path,asset_type=asset_type,table_path= END_data.tables_path + '\\' + asset_type +'.db')
                populate_assets_content_db(pipeline_path=pipeline_path,asset_type=asset_type,table_path= END_data.tables_path + '\\' + asset_type +'.db')





def watchdog(pipeline_path):
    print('Launching watchdog')
    event_handler = MyHandler()  # Create the handler instance
    observer = Observer()       
    print_count = 0 
    observer.schedule(event_handler,pipeline_path, recursive=True)  
    observer.start() 

    try:
        while True:
            time.sleep(3)  # Keep the script running
            print_count +=1
            if print_count % 100 == 0 :
                print(f'watchdog still watchdogging,executed {print_count} times')

    except KeyboardInterrupt:
        observer.stop()  # Stop the observer on user interruption
    observer.join()      # Wait for the thread to finish

watchdog(pipeline_path='\\\\Storage\\esma\\3D4\\threeLittlePigs')