import data
from data import global_variables

from modules.db_interactions.sequences.create_sequence_tables import create_sequences_tables
from modules.db_interactions.sequences.populate_sequences_db import populate_sequences_db,populate_shots_content_db

#create tables
def sequences_db_init():
    'create the tables if they dont exist, and fill them with the data'
    for sequence in global_variables.sequences:
        
        sequence_path = global_variables.sequences_path + '\\' + sequence
        create_sequences_tables(db_creation_path=global_variables.sequences_db_path,db_name= sequence + '.db' ,sequence=sequence)


    for sequence in global_variables.sequences:
        sequence_path = global_variables.sequences_path+ '\\' + sequence

        table_path = global_variables.sequences_db_path +'\\'+sequence+'.db'

        populate_sequences_db(scan_path=global_variables.sequences_path+'\\'+sequence,
                        sequence=sequence,
                        table_path=table_path)
        
        populate_shots_content_db(pipeline_path=global_variables.pipeline_path,
                                sequence=sequence ,
                                table_path=table_path)
        
sequences_db_init()