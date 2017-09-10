import os
import time

from googleapiclient.http import MediaFileUpload

import apiexample


global total_upload_bytes
total_upload_bytes = 0



def items_are_fully_synced():
    return False


def get_file_id(name, parent_id):
    try:
        return list_q_search("'%s' in parents and name='%s' and trashed=false" 
                             % (parent_id, name))['files'][0]['id']
    except:
        return None
    
    
    
def unsynced_dirs():
    return ["/homeframe/jon/Documents/edu/wsc"]
#     return gui.get_active_dirs()


def get_file_metadata(file_id):
#     file_id = get_file_id(name, parent_id)
    return apiexample.get_drive_service().files().get(fileId=file_id).execute()

def get_modified_drive(file_id):
    return apiexample.get_drive_service().files().get(fileId=file_id, fields="modifiedTime").execute()


def is_up_to_date(machine_dir, name, parent_id):
    file_id = get_file_id(name, parent_id)
    if not file_id:
        return False
    local_time = time.ctime(os.path.getmtime(machine_dir))
    drive_time = get_file_metadata(file_id)
    print("file metadata: %s" % drive_time)
    return True
    
    
def drive_file_exists(name, parent_id):
    result = list_q_search("'%s' in parents and name='%s' and trashed=false")



def upload_file(name, machine_dir, parent_id):
    global total_upload_bytes
    total_upload_bytes += os.path.getsize(machine_dir)

    file_metadata = {
            "name": name,
            "parents": [ parent_id ]
                        }
    media = MediaFileUpload(machine_dir,
                            resumable=True)
    file = apiexample.get_drive_service().files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print("uploaded file, id=%s ; metadata: %s" % (file['id'], get_file_metadata(file['id'])))

def get_drive_dir(machine_dir):
    s = apiexample.DRIVE_FOLDER_NAME + "/"
    s += machine_dir.split('/')[-1]
    return s


def is_dir(machine_dir):
    return os.path.isdir(machine_dir)


def list_q_search(q):
    return apiexample.get_drive_service().files().list(fields="files(id, name)", q=q).execute()


def create_drive_folder(name, parent):    
    folder_metadata = {"name": name,
                       "mimeType": "application/vnd.google-apps.folder",
                       "parents": [parent]}

    folder = apiexample.get_drive_service().files().create(body=folder_metadata, fields='id').execute()
    
    print("created folder %s , id=%s" % (name, folder['id']))
    
    return folder['id']

def get_drive_folder_id(parent_id, folder_name):
    '''
    Returns folder id
    '''
    
    search_result = list_q_search(
        "name='%s' and mimeType='application/vnd.google-apps.folder' and '%s' in parents and trashed=false" %
        (folder_name, parent_id))
    
    if len(search_result['files']) >= 1:
        print(search_result)
        return search_result['files'][0]['id']
    else:
        return create_drive_folder(folder_name, parent_id)
    

    
    
def get_dir_files(machine_dir):
    return os.listdir(machine_dir)

def sync_folder_recursively(machine_dir, parent_id):
    for name in get_dir_files(machine_dir):
        item_dir = machine_dir + '/' + name
        if is_dir(item_dir):
            sync_folder_recursively(item_dir, 
                                    get_drive_folder_id(parent_id, name))
        else:
            if not is_up_to_date(item_dir, name, parent_id):
                upload_file(name, item_dir, parent_id)
            else:
                print("file %s up to date" % name)
    
    
    
def new_main():
    pass

    
    
    
    
def main():
    if items_are_fully_synced():
        return
    
    base_folder_id = apiexample.get_config_data(apiexample.get_drive_service())['base_folder_id']
    
    for folder_dir in unsynced_dirs():
        print("main loop for folder dir %s" % folder_dir)
        parent_id = get_drive_folder_id(base_folder_id, folder_dir.split('/')[-1])
        sync_folder_recursively(folder_dir, parent_id)



if __name__ == "__main__":
    main()
    
    print("total bytes uploaded: %s" % total_upload_bytes)
    mb = total_upload_bytes / 1000000
    print("total mb uploaded: %s" % mb)
    


                    
                    
                    
                    