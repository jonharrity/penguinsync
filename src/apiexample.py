from __future__ import print_function
import httplib2
import os
import io
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
DRIVE_FOLDER_NAME = "Drive Client Storage"

CONFIG_FILE_NAME = 'config.json'


CONFIG_KEYS = ['base_folder_id']



def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_drive_service():
    try:
        drive_service
    except:
        global drive_service
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http=http)
    return drive_service


def get_files_app_data_folder(service):
    results = service.files().list(spaces="appDataFolder", fields="files(id, name)").execute()
    items = results.get('files', [])
    files = list((item["name"], item["id"]) for item in items)

    return files



def get_config_file_id(service):
    results = service.files().list(spaces="appDataFolder", fields="files(id, name)").execute()
    items = results.get('files', [])
    files = list((item["name"], item["id"]) for item in items)

    for item in files:
        if item[0] == CONFIG_FILE_NAME:
            return item[1]
        
    return None


def get_config_data(service):
    config_file_id = get_config_file_id(service)
    
    if not config_file_id:
        raise Exception("No config file found.")
    
    request = service.files().get_media(fileId=config_file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        done = downloader.next_chunk()
        
    data = fh.getvalue().decode("utf-8")
    return json.loads(data)


def init_client_drive_data(service):
    file_metadata = {"name": DRIVE_FOLDER_NAME,
                     "mimeType": "application/vnd.google-apps.folder"}
    client_folder = service.files().create(body=file_metadata, fields="id").execute()
    
    print("created client folder, id=%s" % client_folder["id"])
    
    obj = {"base_folder_id": client_folder["id"]}
    
    
    init_config_name = "default_config.json"
    with open(init_config_name, 'w') as init_config_file:
        init_config_file.write(json.dumps(obj))
    
    file_metadata = {
            "name": CONFIG_FILE_NAME,
            "parents": [ "appDataFolder" ]
                        }
    media = MediaFileUpload(init_config_name,
                            mimetype='application/json',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print("created config file, id=%s" % file["id"])



def main():
    service = get_drive_service()
    
    data_folder_files = get_files_app_data_folder(service)
    print("data folder files: %s\n" % data_folder_files)
    
    config_data = get_config_data(service)
    
    if not config_data:
        print("No config data found, creating drive data folder and config file...")
        init_client_drive_data(service)
        print("Done initiating,")
        config_data = get_config_data(service)
    
    print("Read config data:")
    print(config_data)


    results = service.files().list(fields="files(name, id)", q="'%s' in parents" % 
                                   config_data["base_folder_id"]).execute()
    items = results.get("files", [])
    print("\nFiles found in Drive Client Storage:")
    if not items:
        print("(none)")
    else:
        for item in items:
            print("%s (%s)" % (item["name"], item["id"]))
    
    

if __name__ == '__main__':
    main()











