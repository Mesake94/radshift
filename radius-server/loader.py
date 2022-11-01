from dotenv import load_dotenv
import os

load_dotenv()

# read database parameters from the .env file
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

# custom function to update freeradius sql module
def update_content(filepath, search_text, replace_text):
    data = None
    with open(filepath, 'r') as f:
        data = f.read()

        data = data.replace(search_text, replace_text)
    
    if data is not None:
        with open(filepath, 'w') as f:
            f.write(data)

        print(f'{filepath}- contents have been updated')

"""_summary_: Summary of temp postgres connection parameters to be updated

    server = "temp-host"
	port = 5432
	login = "temp-login"
	password = "temp-password"

    radius_db = "radius"
"""

sql_module_path = "/etc/freeradius/3.0/mods-available/sql"

update_content(sql_module_path, 'radius_db = "radius"', f'radius_db = "{DB_NAME}"')
update_content(sql_module_path, 'server = "temp-host"', f'server = "{DB_HOST}"')
update_content(sql_module_path, 'port = 5432', f'port = {DB_PORT}')
update_content(sql_module_path, 'login = "temp-login"', f'login = "{DB_USER}"')
update_content(sql_module_path, 'password = "temp-password"', f'password = "{DB_PASSWORD}"')



    
    








