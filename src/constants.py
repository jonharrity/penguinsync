import os


APPLICATION_NAME = 'Drive API Python Quickstart'


#PATHS
PROGRAM_DIR = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-2])
DATA_DIR = os.path.join(PROGRAM_DIR, 'data')
SRC_DIR = os.path.join(PROGRAM_DIR, 'src')
CREDENTIAL_DIR = os.path.join(os.path.expanduser('~'), '.credentials')
CLIENT_SECRET_DIR = os.path.join(SRC_DIR, 'client_secret.json')
CONFIG_FILE_NAME = 'config.json'


#ON GOOGLE DRIVE 
DRIVE_BASE_DIR = 'Drive Client Storage'
DRIVE_SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata'





#not currently in use
CONFIG_KEYS = ['base_folder_id']

