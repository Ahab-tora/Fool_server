import sqlite3
from pathlib import Path

def create_assets_tables(db_creation_path:str,db_name:str,asset_type:str):
    '''
    create a db for the asset type, two tables.
    table assetType_asset_table with all the assets
    table assetType_data_table linked to the previous table with the data of the assets
    '''
    
    connection = sqlite3.connect(db_creation_path+'\\'+db_name)
    cursor=connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')
    
    cursor.executescript(f'''
    CREATE TABLE IF NOT EXISTS {asset_type}_asset_table(
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    icon_path TEXT
    );

    CREATE TABLE IF NOT EXISTS {asset_type}_data_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    department TEXT NOT NULL,
    status TEXT NOT NULL,
    parent_id INTEGER,
    last_modification TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY (parent_id) REFERENCES {asset_type}_asset_table(asset_id)
    );
    ''')
    
    connection.commit()
    connection.close()


def create_files_tables(db_creation_path:str,db_name:str):
    '''
    table with all the assets , used in the treeview
    '''
    connection = sqlite3.connect(db_creation_path+'\\'+db_name)
    cursor=connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treeview_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    size TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    last_modification TEXT NOT NULL,
    parent TEXT,
    children TEXT
    );''')

    connection.commit()
    connection.close()


def create_publish_table(db_creation_path:str,db_name:str):
    '''
    table used to review things before they are published
    '''
    connection = sqlite3.connect(db_creation_path+'\\'+db_name)
    cursor=connection.cursor()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS publish_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    department TEXT NOT NULL
    );''')

#creation_path = 'D:\\code\\Fool_v3\\data\\projects\\project_template\\files_db'
creation_path = '\\\\Storage\\esma\\3D4\\threeLittlePigs\\pipeline\\END_data\\files_db'

#create_files_tables(db_creation_path=creation_path,db_name='treeview_table.db')
'''
import data.global_variables as global_variables
#types are character,item,prop or set

for asset_type_path in Path(global_variables.assets_path).iterdir():
    asset_type_name = str(asset_type_path).split('\\')[-1]
    create_assets_tables(db_creation_path=global_variables.databases_path,db_name= asset_type_name + '.db',asset_type = asset_type_name )
'''
'''create_assets_tables(db_creation_path=creation_path,db_name='character.db',asset_type='character')
create_assets_tables(db_creation_path=creation_path,db_name='item.db',asset_type='item')
create_assets_tables(db_creation_path=creation_path,db_name='prop.db',asset_type='prop')
create_assets_tables(db_creation_path=creation_path,db_name='set.db',asset_type='set')'''


#create_publish_table(db_creation_path=creation_path,db_name='publish.db')

