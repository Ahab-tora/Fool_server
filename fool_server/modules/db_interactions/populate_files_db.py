import sqlite3


from .query_data import get_data_from_file,fetch_all_files,get_assets,get_assets_content


from .insert_data import bulk_insert_data_to_treeview_table,insert_data_to_asset_table,insert_asset_content_data



import time
start = time.time()

def populate_files_treeview_db(scan_path:str,table_path:str):
    '''
    get all the files in directory and their data, and insert it to the database
    
    '''
    connection = sqlite3.connect(table_path)
    cursor=connection.cursor()
    
    batch_size = 1000
    batch = 0
    file_data_list = []
    file_data_list.append(get_data_from_file(file_path=scan_path)) 
    for file in fetch_all_files(scan_path=scan_path):
        file_data_list.append(get_data_from_file(file_path=file)) 
        batch +=1

        if batch == batch_size:
            bulk_insert_data_to_treeview_table(table_path=table_path,file_data_list=file_data_list,manage_connection=False,cursor=cursor)
            batch = 0
            file_data_list.clear()

    if file_data_list:
        bulk_insert_data_to_treeview_table(table_path=table_path,file_data_list=file_data_list,manage_connection=False,cursor=cursor)
        
    connection.commit()
    connection.close()



def populate_assets_db(scan_path:str,asset_type:str,table_path:str):
    
    assets = get_assets(scan_path=scan_path)

    insert_data_to_asset_table(table_path=table_path,assets=assets,asset_type=asset_type,manage_connection=True)


def populate_assets_content_db(pipeline_path:str,asset_type:str,table_path:str):
    
    data = get_assets_content(pipeline_path=pipeline_path,asset_type=asset_type,table_path=table_path)
    insert_asset_content_data(table_path=table_path,asset_type=asset_type,manage_connection=True,data=data)

    '''try:
        insert_asset_content_data(table_path=table_path,asset_type=asset_type,manage_connection=True,data=data)
    except Exception as e:
        print('populate_assets_content_db error:',e)
    return data'''

table_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\pipeline\\END_data\\files_db'
scan_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs'
#populate_files_treeview_db(scan_path=scan_path,table_path=table_path+'\\treeview_table.db')

#Er1XywQWzLEc51517X



'''populate_assets_db(scan_path=pipeline_path+item_path,asset_type='item',table_path=table_path+'\\item.db')
populate_assets_content_db(pipeline_path=pipeline_path,asset_type='item',table_path=table_path+'\\item.db')

populate_assets_db(scan_path=pipeline_path+character_path,asset_type='character',table_path=table_path+'\\character.db')
populate_assets_content_db(pipeline_path=pipeline_path,asset_type='character',table_path=table_path+'\\character.db')

populate_assets_db(scan_path=pipeline_path+prop_path,asset_type='prop',table_path=table_path+'\\prop.db')
populate_assets_content_db(pipeline_path=pipeline_path,asset_type='prop',table_path=table_path+'\\prop.db')

populate_assets_db(scan_path=pipeline_path+set_path,asset_type='set',table_path=table_path+'\\set.db')
populate_assets_content_db(pipeline_path=pipeline_path,asset_type='set',table_path=table_path+'\\set.db')
'''
