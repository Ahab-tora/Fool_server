import sqlite3
from pathlib import Path

def create_sequences_tables(db_creation_path:str,db_name:str,sequence:str):
    '''
    create a db for the asset type, two tables.
    table assetType_asset_table with all the assets
    table assetType_data_table linked to the previous table with the data of the assets
    '''
    
    connection = sqlite3.connect(db_creation_path+'\\'+db_name)
    cursor=connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')
    
    cursor.executescript(f'''
    CREATE TABLE IF NOT EXISTS {sequence}_shots_table(
    shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    icon_path TEXT
    );

    CREATE TABLE IF NOT EXISTS {sequence}_data_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    department TEXT NOT NULL,
    status TEXT NOT NULL,
    parent_id INTEGER,
    last_modification TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY (parent_id) REFERENCES {sequence}_data_table(shot_id)
    );
    ''')
    
    connection.commit()
    connection.close()

