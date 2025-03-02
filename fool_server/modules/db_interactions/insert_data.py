import sqlite3


def bulk_insert_data_to_treeview_table(table_path:str,file_data_list:list,manage_connection:bool,cursor) :
    '''
    Insert into the treeview_table a list of tuples containing the  name, type, path, size, creation_date, 
    last_modification, parent, children for each item
    '''
    print('Launching bulk insert')

    
    if manage_connection is True:
        connection = sqlite3.connect(table_path)
        cursor=connection.cursor()

    cursor.executemany('''
    INSERT OR REPLACE INTO treeview_table(
        name, type, path, size, creation_date, 
        last_modification, parent
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', file_data_list)

    if manage_connection is True:
        connection.commit()
        connection.close()


def insert_asset_content_data(table_path:str,asset_type:str,manage_connection:bool,data:list,cursor=None):
    print('launching insert asset content data')
    try:
        if manage_connection is True:
            connection = sqlite3.connect(table_path)
            cursor=connection.cursor()


        cursor.executemany(f'''
        INSERT OR IGNORE INTO {asset_type}_data_table (
        name,path,type,department,status,parent_id,last_modification)
        VALUES (?,?,?,?,?,?,?)
            ''',data)

        if manage_connection is True:
            connection.commit()
            connection.close()
    except Exception as e:
        print('insert_asset_content_data error:',e)
        


    


def insert_data_to_asset_table(table_path:str,assets:list,asset_type:str,manage_connection:bool,cursor=None):
    try:
        if manage_connection is True:
            connection = sqlite3.connect(table_path)
            cursor=connection.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')

        for asset_path in assets:
        
            asset_name = asset_path.name.split('\\')[-1]
            if asset_path.is_dir() and any(asset_path.iterdir()):  
                #data as tuple for sqlite
                data = (asset_name,str(asset_path),asset_type)
                #print(data)
                cursor.execute(f'''
                INSERT OR IGNORE INTO '{asset_type}_asset_table'
                (name,path,type)
                VALUES (?, ?, ?)
                ''', data)

        if manage_connection is True:
            connection.commit()
            connection.close()
    except Exception as e:
        print('error at insert_data_to_asset_table',e)