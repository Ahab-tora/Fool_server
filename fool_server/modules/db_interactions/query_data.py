from pathlib import Path
import datetime
import uuid
import time
import sqlite3

import data
from data import global_variables

def get_assets(scan_path:str):
    'get all the assets from a path (one layer scan)'
    try:
        folder = Path(scan_path)
        assets_list = []

        for entry in folder.iterdir():
            assets_list.append(entry)

        return assets_list
    except Exception as e:
        print('error at get_assets',e)
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
    
'''def get_assets_content_data(entry,department,status,parent_id):
    try:
        file = Path(entry)
        data = [] 

        if file.is_dir():
            for sub_entry in file.iterdir():
                data.extend(get_assets_content_data(sub_entry, department, status, parent_id)) 

        else:
            name = file.name
            path = str(file)
            file_type = file.suffix.lstrip('.') or "unknown"
            last_modification = str(datetime.datetime.fromtimestamp(file.stat().st_mtime))
            data.append((name, path, file_type, department, status, parent_id, last_modification))

        return data
    except:
        print(f'error at get_assets_content_data for {entry,department,status,parent_id}')
        return []'''
                        
def get_assets_content_data(entry,department,status,parent_id):
    'returns metadata of a file as tuple, is recursive'
    try:                   
        file = Path(entry)
        if file.is_dir() == True:
            for entry in file.iterdir():
                get_assets_content_data(entry=entry,department=department,status=status,parent_id=parent_id)

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
        print('Error at get_assets_content_data:',e)
        return []

def get_assets_content(pipeline_path:str,asset_type:str,table_path:str)->list:
    '''
    returns a list of tuples with the data of each file in the departments list (maya)
    '''
    print('launching get assets_content')
    try:
        connection = sqlite3.connect(table_path)
        cursor = connection.cursor()

        assets_content_list = []

        maya_departments_list = 'assetLayout','cloth','dressing','groom','lookdev','modeling','rig'
        status_list = 'edit','publish'

        houdini_departments_list = 'abc','audio','comp','desk','flip','geo','hdz','render','scripts','sim','tex','video'

        #asset_type_path = Path(pipeline_path + '\\04_asset' + '\\' + asset_type)
        asset_type_path = Path(global_variables.assets_path + '\\' + asset_type)


        for asset in asset_type_path.iterdir():
            
            asset_name = str(asset).split('\\')[-1]

            cursor.execute(f'''SELECT asset_id FROM {asset_type}_asset_table
            WHERE name = ?;
            ''', (asset_name,))
            try:
                parent_id = cursor.fetchone()[0]
            except:
                continue

            #maya data
            
            for status in status_list:
                
                for department in maya_departments_list:
                    try:
                        asset_content_path = Path(str(asset_type_path) + '\\' + asset_name + '\\maya\\scenes' + '\\' + status + '\\' + department)

                        for entry in asset_content_path.iterdir():
                            
                            data = get_assets_content_data(entry=entry,department=department,status=status,parent_id=parent_id)
                            assets_content_list.append(data)
                    except Exception as e:
                        print(f'error in get_assets_content while getting maya data : {e}')


            #houdini data
            for department in houdini_departments_list:
                    try:
                        asset_content_path = Path(str(asset_type_path) + '\\' + asset_name + '\\houdini' + '\\' + department)

                        for entry in asset_content_path.iterdir():
                            
                            data = get_assets_content_data(entry=entry,department=department,status='None',parent_id=parent_id)
                            assets_content_list.append(data)
                    except Exception as e:
                        print(f'error in get_assets_content while getting houdini data : {e}')
        connection.close()
    except Exception as e:
        print('get_assets_content error:',e)
        return []
    #print('-----------------------------------',assets_content_list)
    return assets_content_list

    #pipeline_path + '\\04_asset' + '\\' + asset_type + '\\maya\\scenes' + '\\' + status
    
#get_assets_content(pipeline_path='\\\\Storage\\esma\\3D4\\threeLittlePigs',table_path= 'D:\\code\\Fool_v3\\data\\projects\\project_template\\files_db\\character.db',asset_type='character')
    
 

def size_converter(size):
    return size


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


def set_children(table_path):
    '''
    Update the children of each folder with decendants
    '''
    #connection
    connection = sqlite3.connect(table_path)
    cursor=connection.cursor()
    
    cursor.execute('''SELECT id, parent , path FROM treeview_table''')
    all = cursor.fetchall()
    
    #we create a dict 
    hierarchy_dict = {}
    for element in all:
        hierarchy_dict[element[2]] = []

    #we have a hash map with every file
    #for every element, we check if the parent is the same as the key,if yes, we append the id to the key

    for element in all:
        if element[1] in hierarchy_dict:
            hierarchy_dict[element[1]].append(element[0])

    empty_list = []

    for key in hierarchy_dict:
        if not hierarchy_dict[key]:
            empty_list.append(key)
            continue
        
    for key in empty_list:
        del hierarchy_dict[key]


    #we switch the data to have an acceptable tuple for sqlite
    #then we need to translate the list of children to a string and we replace [ and ] by nothing
    #it's a pain

    def convert_ids_to_str(ids:list) -> str:
        empty_str = ''
        ids_str = [empty_str+str(element) for element in ids]
        ids_str = ','.join(ids_str)
        return(ids_str)

    data = [((convert_ids_to_str(children),path)) for path, children in hierarchy_dict.items()]

    print(data)

    query = '''UPDATE treeview_table SET children = ? WHERE path = ? '''
    cursor.executemany(query, data)
    connection.commit()
    connection.close()


'''start = time.time()
table_path = table_path = 'D:\\code\\Fool_v3\\data\\projects\\project_template\\files_db\\treeview_table.db'
set_children(table_path=table_path)
end = time.time()

print(f'Executed in {end-start}s')
'''