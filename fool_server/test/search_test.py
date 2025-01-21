
import sqlite3
import PySide6
from PySide6.QtCore import Qt, QAbstractTableModel, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel
import sys
from pathlib import Path
import ftrack_api
import time
from datetime import datetime
import pprint

api_key = 'YWUwZGY2MGEtYjA4NS00NzcyLThjYzItNTk4NTJkODQ5MWNiOjo2YjZkNjA0Ni00NDZmLTQ4YTctODU3Yy0zNzQ2MDc0M2FmNTk'
api_user = 'e.guinet-elmi@lyn.ecolescreatives.com'
server_url = 'https://esma-lyon.ftrackapp.com'
project = 'END'

session = ftrack_api.Session(
server_url=server_url,
api_key=api_key,
api_user=api_user,)

#workers = session.query(f'''Asset_ where parent.name is {type}''').all()

folder_name = '05_asset'
parent_item = 'Alberto'
            #tasks = session.query(f'''Task where parent.name is {parent_item.name_item} and project.name is {project_name}''').all()
task = session.query(f'''Task where project.name is {project}
                                    and  parent.parent.parent.name is {folder_name}
                                    and  parent.name is {parent_item}''').first()

for x in task['type']['name']:
    print(x)

session.close()


'''
object_type_id
priority_id
id
bid
time_logged
bid_time_logged_difference
description
start_date
end_date
status_id
thumbnail_source_id
type_id
project_id
sort
type
status
project
priority
object_type
metadata
ancestors
descendants
lists
incoming_links
outgoing_links
status_changes
split_parts
context_type
name
parent_id
thumbnail_id
thumbnail_url
thumbnail
parent
children
appointments
assignments
allocations
assets
timelogs
scopes
notes
_link
link
managers
created_by_id
created_at
created_by
custom_attributes


id
type
resource_id
context_id
context
resource


resource_type
username
is_active
require_details_update
is_otp_enabled
is_totp_enabled
timelogs
task_type_links
memberships
metadata
user_security_roles
user_type_id
user_type
custom_attributes
first_name
last_name
email
thumbnail_id
thumbnail_url
thumbnail
id
appointments
assignments
allocations
dashboard_resources
'''