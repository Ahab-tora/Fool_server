import sqlite3



def insert_shot_content_data(table_path:str,sequence:str,manage_connection:bool,data:list,cursor=None):
    print('launching insert shot content data')
    try:
        if manage_connection is True:
            connection = sqlite3.connect(table_path)
            cursor=connection.cursor()


        cursor.executemany(f'''
        INSERT OR IGNORE INTO {sequence}_data_table (
        name,path,type,department,status,parent_id,last_modification)
        VALUES (?,?,?,?,?,?,?)
            ''',data)

        if manage_connection is True:
            connection.commit()
            connection.close()

    except Exception as e:
        print('insert_shot_content_data error:',e)
        

def insert_data_to_sequence_table(table_path:str,shots:list,sequence:str,manage_connection:bool,cursor=None):
    try:
        if manage_connection is True:
            connection = sqlite3.connect(table_path)
            cursor=connection.cursor()

        cursor.execute('PRAGMA foreign_keys = ON;')

        for shot_path in shots:
        
            shot_name = shot_path.name.split('\\')[-1]
            if shot_path.is_dir() and any(shot_path.iterdir()):  
                #data as tuple for sqlite
                data = (shot_name,str(shot_path),)
                #print(data)
                cursor.execute(f'''
                INSERT OR IGNORE INTO '{sequence}_shots_table'
                (name,path)
                VALUES (?,?)
                ''', data)

        if manage_connection is True:
            connection.commit()
            connection.close()
    except Exception as e:
        print('error at insert_data_to_sequence_table',e)
    

