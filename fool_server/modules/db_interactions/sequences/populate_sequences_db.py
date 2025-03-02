import sqlite3


from .query_data_sequences import get_data_from_file,fetch_all_files,get_shots,get_shots_content


from .insert_data_sequences import insert_data_to_sequence_table,insert_shot_content_data



import time




def populate_sequences_db(scan_path:str,sequence:str,table_path:str):
    
    shots = get_shots(scan_path=scan_path)

    insert_data_to_sequence_table(table_path=table_path,shots=shots,sequence=sequence,manage_connection=True)


def populate_shots_content_db(pipeline_path:str,sequence:str,table_path:str):
    
    data = get_shots_content(sequence=sequence,table_path=table_path)
    insert_shot_content_data(table_path=table_path,sequence=sequence,manage_connection=True,data=data)
