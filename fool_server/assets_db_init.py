import data
from data import global_variables

from modules.db_interactions.create_tables import create_assets_tables
from modules.db_interactions.populate_files_db import populate_assets_db,populate_assets_content_db

#create tables

for asset_type in global_variables.assets_types:
    asset_type_path = global_variables.assets_path + '\\' + asset_type
    asset_type_name = str(asset_type_path).split('\\')[-1]
    create_assets_tables(db_creation_path=global_variables.databases_path,db_name= asset_type_name + '.db',asset_type = asset_type_name )

#populate asset_tables
for asset_type in global_variables.assets_types:
    asset_type_path = global_variables.assets_path + '\\' + asset_type

    asset_type_name = str(asset_type_path).split('\\')[-1]
    table_path = global_variables.databases_path +'\\'+asset_type_name+'.db'

    populate_assets_db(scan_path=global_variables.assets_path+'\\'+asset_type_name,
                       asset_type=asset_type_name ,
                       table_path=table_path)
    populate_assets_content_db(pipeline_path=global_variables.pipeline_path,
                               asset_type=asset_type_name ,
                               table_path=table_path)