import ftrack_api


api_key = 'YWUwZGY2MGEtYjA4NS00NzcyLThjYzItNTk4NTJkODQ5MWNiOjo2YjZkNjA0Ni00NDZmLTQ4YTctODU3Yy0zNzQ2MDc0M2FmNTk'
api_user = 'e.guinet-elmi@lyn.ecolescreatives.com'
server_url = 'https://esma-lyon.ftrackapp.com'
project = 'END'
















'''def create_asset_ftrack(asset_name):
    user = session.query(f'User where last_name is {user_last_name}').first()
    asset_type = session.query(f'Type where name is prop').one()
    new_asset = session.create('Asset_',{
        'name':asset_name,
        'parent':parent_family,
        'type':asset_type},)
    e.guinet-elmi@lyn.ecolescreatives.com'''

aa= {   'SQ0010': {   'end_date': '<Arrow [2024-12-30T23:00:00+00:00]>',
                  'status': 'WIP'},
    'dialogues': {   'end_date': '<Arrow [2024-12-27T23:00:00+00:00]>',
                     'status': 'WIP'},
    'designs': {   'end_date': '<Arrow [2024-11-14T10:00:00+00:00]>',
                   'status': 'WIP'}}

for key in aa:
    print(key)