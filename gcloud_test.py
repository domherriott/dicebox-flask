from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

from io import BytesIO

import pandas as pd
import requests





SPREADSHEET_ID = '1n08s5eRAuO2er22mtPVVFz5_i2YGbi1sRHgcypVUB-o'

# setup google drive
credentials = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=['https://www.googleapis.com/auth/drive']
    )


def add_logs():

    def log_file_exists():
        return
    
    def create_log_file():
        return
    
    def add_logs():
        return
    
    if log_file_exists == False:
        create_log_file()

    add_logs()
    
    return

def get_data():
    service = build("sheets", "v4", credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range='A:F')
        .execute()
    )
    values = result.get("values", [])
    print(values)

    return

get_data()

'''
# Replace 'FOLDER_NAME' with the name you want to give your new folder
folder_name = 'Test Upload'

service = build("drive", "v3", credentials=credentials)
folder_metadata = {
    'name': folder_name,
    "parents": ['1NG4fuZk9E9bqaaksKSxNFcr1YtU4tKlH'],
    'mimeType': 'application/vnd.google-apps.folder'
}

# create folder 
new_folder = service.files().create(body=folder_metadata).execute()


#upload file inside the folder
file_metadata = {'name': 'image.webp', 'parents': [new_folder['id']]}
media = MediaFileUpload('dom.png')
file = service.files().create(body=file_metadata, media_body=media).execute()

# list the file inside of the folder
results = service.files().list(q=f"'{new_folder['id']}' in parents", fields="files(name)").execute()
items = results.get('files', [])
print(f"Files inside the folder , {items}")
'''