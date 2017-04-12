
import pickle
import time
import httplib2
import os
import io
import json

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client import client



# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

CONFIG_FILE_NAME = 'config.json'
CONFIG_KEYS = ['base_folder_id']


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


"""
todo:
    
    when a path is removed from monitoring, optionally remove from drive
    
"""
    


class SyncServer:
    
    
    def __init__(self, save_path):
        
        self.save_path = save_path
        
        self.init_drive_service()#self.drive_service
        self.load_config_data()#self.drive_parent_id
        
        self.drive_ids = self.load_drive_ids()#self.drive_ids
        self.last_synced = self.load_last_synced()#self.last_synced
        self.active_dirs = self.load_active_dirs()#self.active_dirs
        
        self.unsynced_files = set()
        self.sync()
        
        
    def load_config_data(self):
        data = self.get_config_data()
        self.drive_parent_id = data['base_folder_id']
        
            
    def get_config_file_id(self):
        results = self.drive_service.files().list(spaces="appDataFolder", fields="files(id, name)").execute()
        items = results.get('files', [])
        files = list((item["name"], item["id"]) for item in items)
    
        for item in files:
            if item[0] == CONFIG_FILE_NAME:
                return item[1]
            
        return None
    
    
    def get_config_data(self):
        config_file_id = self.get_config_file_id()
        
        if not config_file_id:
            raise Exception("No config file found.")
        
        request = self.drive_service.files().get_media(fileId=config_file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
    
        done = False
        while not done:
            done = downloader.next_chunk()
            
        data = fh.getvalue().decode("utf-8")
        return json.loads(data)
        
        
        
    def init_drive_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http=http)
        
        
        
    def get_credentials(self):
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
    
    
    def load_active_dirs(self):
        file = open(self.save_path + "/adr", 'rb')
        active_dirs = pickle.load(file)
        file.close()
        return active_dirs
    
    def save_active_dirs(self):
        file = open(self.save_path + "/adr", 'wb')
        pickle.dump(self.active_dirs, file)
        file.close()

        
    def load_drive_ids(self):
        file = open(self.save_path + "/did", 'rb')
        drive_ids = pickle.load(file)
        file.close()
        return drive_ids

    def save_drive_ids(self):
        file = open(self.save_path + "/did", 'wb')
        pickle.dump(self.drive_ids, file)
        file.close()
                
        
    def load_last_synced(self):
        file = open(self.save_path + "/lsy", 'rb')
        last_synced = pickle.load(file)
        file.close()
        return last_synced
    
    def save_last_synced(self):
        file = open(self.save_path, "/lsy", 'wb')
        pickle.dump(self.last_synced, file)
        file.close()
        
        
    def detect_unsynced_files(self):
        for path in self.last_synced.keys():
            if time.mktime(self.last_synced[path]) - os.path.getmtime(path) < 0:
                self.unsynced_files.add(path)
                
                
    def sync_all_unsynced(self):
        for path in self.unsynced_files:
            self.update_file(path)
        self.unsynced_files.clear()
    
    
    
    def update_file(self, path):
        media = MediaFileUpload(path, resumable=True)
        self.drive_service.files().update(fileId=self.drive_ids[path], media_body=media.execute())
        print("updated file: %s" % path)
    
    
    def create_file(self, path):
        media = MediaFileUpload(path, resumable=True)
        file_metadata = {
            "name": path.split('/')[-1],
            "parents": [ self.drive_parent_id ]
                        }
        result = self.drive_service.files().create(body=file_metadata, media_body=media, 
                                                   fields='id').execute()
        return result['id']
    
    
    
    #recursively returns list of subfiles, NOT including subdirs
    def get_machine_subfiles(self, path):
        subfiles = []
        for subpath in os.listdir(path):
            if os.path.isfile(subpath):
                subfiles.append(subpath)
            else:
                subfiles.extend(self.get_machine_subfiles(subpath))
        
        return subfiles
    
    
    def remove_path_from_monitoring(self, path):
        if path in self.active_dirs:
            self.active_dirs.remove(path)
            self.save_active_dirs()
        
        if os.path.isfile(path):
            self.last_synced.pop(path)
            self.drive_ids.pop(path)
        else:
            for file in self.get_machine_subfiles(path):
                self.last_synced.pop(file, None)
                self.drive_ids.pop(file, None)

        self.save_last_synced()
        self.save_drive_ids()
                
    
    
    def add_new_active(self, path):
        
        if os.path.isdir(path):
            self.add_new_dir(path)
        else:
            self.add_new_file(path)
        
            
    def add_new_dir(self, path):
        self.active_dirs.append(path)
        self.save_active_dirs()
        
        for subfile in self.get_machine_subfiles(path):
            self.drive_ids[subfile] = self.create_file(subfile)
            self.last_synced[subfile] = time.localtime()
        
        self.save_drive_ids()
        self.save_last_synced()
            
    def add_new_file(self, path):
        new_id = self.create_file(path)
        
        self.drive_ids[path] = new_id
        self.last_synced[path] = time.localtime()
        self.active_dirs.append(path)
        
        self.save_active_dirs()
        self.save_drive_ids()
        self.save_last_synced()
            
            
            
            
            
    def sync(self):
        self.detect_unsynced_files()
        self.sync_all_unsynced()
            
            
            
            
            
            
            
            
    
    