from pathlib import Path
import datetime
import uuid
import time
import sqlite3

import data
from data import global_variables

def get_shots(scan_path:str):
    'get all the shots from a path (one layer scan)'
    try:
        folder = Path(scan_path)
        shots_list = []

        for entry in folder.iterdir():
            shots_list.append(entry)

        return shots_list
    except Exception as e:
        print('error at get_shots',e)
        return None


def fetch_all_files(scan_path: str):
    '''
    yields the files from a path, and recursivly yields the children
    '''
    try:
        folder = Path(scan_path)
        for entry in folder.iterdir():
                yield str(entry)
                if entry.is_dir():
                    yield from fetch_all_files(scan_path=entry)
    except Exception as e:
        print(f'Error at fetch all files:{e}')
    
                       
def get_shots_content_data(entry,department,status,parent_id):
    'returns metadata of a file as tuple, is recursive'
    try:                   
        file = Path(entry)
        if file.is_dir() == True:
            for entry in file.iterdir():
                get_shots_content_data(entry=entry,department=department,status=status,parent_id=parent_id)

        name = str(entry).split('\\')[-1] #name
        path = str(entry) #path
        file_type = entry.suffix.lstrip('.') or "unknown" #type
        department = department #department
        status = status #status
        parent_id = parent_id #parent id 
        #modification date
        file_stat = file.stat()
        last_modification = str(datetime.datetime.fromtimestamp(file_stat.st_mtime))

        return (name,path,file_type,department,status,parent_id,last_modification)
    
    except Exception as e:
        print('Error at get_shots_content_data:',e)
        return []


def get_shots_content(sequence:str,table_path:str)->list:
    '''
    returns a list of tuples with the data of each file in the departments list (maya)
    '''
    print('launching get shots_content')
    try:
        connection = sqlite3.connect(table_path)
        cursor = connection.cursor()

        shots_content_list = []

        #maya_departments_list = 'anim','layout','render'
        #status_list = 'edit','publish'

        #houdini_departments_list = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

        #asset_type_path = Path(pipeline_path + '\\04_asset' + '\\' + asset_type)
        sequence_path = Path(global_variables.sequences_path + '\\' + sequence)


        for shot in sequence_path.iterdir():
            
            shot_name = str(shot).split('\\')[-1]

            cursor.execute(f'''SELECT shot_id FROM {sequence}_shots_table
            WHERE name = ?;
            ''', (shot_name,))
            try:
                parent_id = cursor.fetchone()[0]
            except:
                continue

            #maya data
            #for status in global_variables.sequences_status:
            for department in global_variables.sequences_maya_departments:
                
                #for department in global_variables.sequences_maya_departments:
                for status in global_variables.sequences_status:
                    try:
                        shot_content_path = Path(str(sequence_path) + '\\' + shot_name + '\\maya\\scenes' + '\\' + department + '\\' + status)

                        for entry in shot_content_path.iterdir():
                            
                            data = get_shots_content_data(entry=entry,department=department,status=status,parent_id=parent_id)
                            shots_content_list.append(data)
                    except Exception as e:
                        print(f'error in get_shots_content while getting maya data : {e}')


            #houdini data
            for department in global_variables.sequences_houdini_departments:
                    try:
                        shot_content_path = Path(str(sequence_path) + '\\' + shot_name + '\\houdini' + '\\' + department)

                        for entry in shot_content_path.iterdir():
                            
                            data = get_shots_content_data(entry=entry,department=department,status='None',parent_id=parent_id)
                            shots_content_list.append(data)
                    except Exception as e:
                        print(f'error in get_shots_content while getting houdini data : {e}')
        connection.close()
    except Exception as e:
        print('get_shots_content error:',e)
        return []
    return shots_content_list


def get_data_from_file(file_path: str) -> tuple:
    """
    Returns a tuple with file information in this order:
    name, type, path, size, creation_date, last_modification, parent, children
    """
    file = Path(file_path)
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
        creation_date,
        last_modification,
        parent
    )





'''start = time.time()
table_path = table_path = 'D:\\code\\Fool_v3\\data\\projects\\project_template\\files_db\\treeview_table.db'
set_children(table_path=table_path)
end = time.time()

print(f'Executed in {end-start}s')
'''