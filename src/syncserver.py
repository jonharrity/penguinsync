
import time
import os
import io
import json
import socket

import driveids, lastsynced, managedfolders
import constants
import auth

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import tools


import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()






"""
todo:
    
*    when a path is removed from monitoring, optionally remove file from drive
    
*    check for newly added or removed files/directories
        - O(N^2) with current organization to validate each file in last_synced ??
        
*    recursively add  nested subfolders (currently does not check when adding folders)


*    verifying of files/dirs before attempting to upload
    and in create_file: remove create file on system, should raise exception if path is nonexistent

"""



class SyncServer:
    
    
    def __init__(self, save_path, enable_drive_service=True):
                
        self.save_path = save_path
        self.last_synced_time = 'error'
        self.count_upload_total = 0
        
        self.callbacks_finish_sync = []
        self.callbacks_on_login = []
        self.callbacks_on_logout = []
        
        self.drive_service_is_active = False
        
        if enable_drive_service:
            self.startup_drive_service()#self.drive_service
                        
        self.drive_ids = driveids.DriveIds()
        self.last_synced = lastsynced.LastSynced()
        self.managed_folders = managedfolders.ManagedFolders()
        
        self.unsynced_files = set()
        self.sync()
                
                
        self.done_init = True
        
        
        
        
    # * - * - * - *
    # CALLBACK REGISTERS
    # * - * - * - *   
    
    def register_on_sync(self, callback):
        self.callbacks_finish_sync.append(callback)
    
    def register_on_login(self, callback):
        self.callbacks_on_login.append(callback)
        
    def register_on_logout(self, callback):
        self.callbacks_on_logout.append(callback)
        
        
    # * - * - * - *
    # CONFIG DATA on user's drive
    # * - * - * - *
    
        
    def load_config_data(self):
        data = self.get_config_data()
        self.drive_parent_id = data['base_folder_id']
        
        
    def get_config_file_id(self):
        results = self.drive_service.files().list(spaces="appDataFolder", fields="files(id, name)").execute()
        items = results.get('files', [])
        files = list((item["name"], item["id"]) for item in items)
    
        for item in files:
            if item[0] == constants.CONFIG_FILE_NAME:
                return item[1]
            
        return None
    
    
    def get_config_data(self):
        config_file_id = self.get_config_file_id()
        
        if not config_file_id:
            config_file_id = self.init_config_file()
        
        request = self.drive_service.files().get_media(fileId=config_file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
    
        done = False
        while not done:
            done = downloader.next_chunk()
            
        data = fh.getvalue().decode("utf-8")
        return json.loads(data)
        
        
    def init_config_file(self):
        
        
    # * - * - * - *
    # CONNECTING WITH OAUTH2.0
    # * - * - * - *    
    
    
    
    def startup_drive_service(self):
        auth.request_drive_service(self.resolve_drive_service)
        
    def resolve_drive_service(self, drive_service):
        if drive_service:
            self.drive_service = drive_service
            self.load_config_data()
            self.drive_service_is_active
            
            for callback in self.callbacks_on_login:
                try:
                    callback()
                except:
                    pass
        else:
            self.drive_service = None
            self.drive_service_is_active = False
            
        
    
        
    def login(self, callback):
        if self.is_logged_in():
            return

        self.startup_drive_service()
        
    def logout(self):
        auth.destroy_credentials()
        self.drive_service = None
        self.drive_service_is_active = False
        
        for callback in self.callbacks_on_logout:
            try:
                callback()
            except:
                pass
    
    def is_logged_in(self):
        try:
            if self.drive_service:
                return True
        except:
            return False

    def is_connected_to_internet(self):
        url = 'www.google.com'
        try:
            host = socket.gethostbyname(url)
            socket.create_connection((host, 80), 2)
            return True
        except:
            return False
        
    
    # * - * - * - *
    # SYNC TASKS
    # * - * - * - *    
        
    
    def get_total_upload_size(self):
        return self.count_upload_total
    
        
    def detect_unsynced_files(self):
        paths_to_remove = []
        for path in self.last_synced.keys():
            try:
                if time.mktime(self.last_synced[path]) - os.path.getmtime(path) < 0:
                    self.unsynced_files.add(path)
            except os.error:
                print("file removal detected of path %s" % path)
                paths_to_remove.append(path)
                
        for path in paths_to_remove:
            self.remove_path_from_monitoring(path)
                
                
                
    def sync_all_unsynced(self):
        for path in self.unsynced_files:
            self.update_file(path)
        self.unsynced_files.clear()
    
    
    
    def update_file(self, path):
#         if not os.path.isfile(path):
#             raise Exception('Can not update [' + path + ']: file not found')
        
        
        self.count_upload_total += os.path.getsize(path)
        media = MediaFileUpload(path, resumable=True)
        self.drive_service.files().update(fileId=self.drive_ids[path], media_body=media).execute()
        self.last_synced[path] = time.localtime()
    
    
    def create_file(self, path):
        file_size = os.path.getsize(path)
        self.count_upload_total += file_size
        
        if file_size == 0:
            file = open(path, 'wb')
            file.write('\n'.encode('UTF-8'))
            file.close()
            print('created nonexistent file ' + path)
        
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
        if path == '' or path[-1] != '/':
            path += '/'
            
        for subpath in os.listdir(path):
            full_subpath = path + subpath
            if os.path.isfile(full_subpath):
                subfiles.append(full_subpath)
            else:
                subfiles.extend(self.get_machine_subfiles(full_subpath))
        
        return subfiles
    
    
    def remove_path_from_monitoring(self, path):
        if path in self.managed_folders.keys():#path is folder
            self.managed_folders.remove(path)
            #remove subpaths from monitoring
            i = 0
            while i < len(self.managed_folders):
                folder = self.managed_folders[i]
                if len(folder) <= path:
                    i += 1
                else:
                    if folder[:len(path)] == path:
                        self.managed_folders.pop(i)

                        
            for file in self.get_machine_subfiles(path):
                try:
                    self.last_synced.pop(file, None)
                    self.drive_ids.pop(file, None)
                except:
                    pass
        else:#path is a file
            self.last_synced.pop(path)
            self.drive_ids.pop(path)
                
        self.save_last_synced()
        self.save_drive_ids()
        self.save_managed_folders()
 
            
    def add_new_dir(self, path, do_add_all):
        
        if path in self.managed_folders:
            print('requested add dir %s, but folder is already listed for syncing')
            return
        
        self.managed_folders.append(path)
        
        if not self.drive_service_is_active:
            return
        
        if do_add_all:
            for subfile in self.get_machine_subfiles(path):
                self.drive_ids[subfile] = self.create_file(subfile)
                self.last_synced[subfile] = time.localtime()
            self.save_drive_ids()
            self.save_last_synced()
            
        self.save_managed_folders()
            
    def add_new_file(self, path):
        
        if path in self.drive_ids.keys():
            print('requested add path %s, but path is already listed for syncing' % path)
            return
        
        if not self.drive_service_is_active:
            return
        
        try:
            new_id = self.create_file(path)
            
            print('created file...')
            
            self.drive_ids[path] = new_id
            self.last_synced[path] = time.localtime()
    
        except:
            print('error while adding %s' % path)
         
    def detect_new_files(self):
        for folder in self.managed_folders:
            for path in os.listdir(folder):
                path = folder + '/' + path
                if os.path.isfile(path):
                    if not path in self.drive_ids.keys():
                        self.add_new_file(path)
                else:
                    if not path in self.managed_folders:
                        self.add_new_dir(path)
                        
            
            
            
    def sync(self):
              
        if not self.drive_service_is_active:
            return
        
#         self.detect_new_files()
        self.detect_unsynced_files()
        self.sync_all_unsynced()
        self.last_synced_time = time.localtime()
            
        print('completed: successful sync; t=%s' % str(self.last_synced_time))
            
        for callback in self.callbacks_finish_sync:
            try:
                callback()
            except:
                pass
            
            
            
            
            
            
            
            
            
    
    