import os


APPLICATION_NAME = 'Drive API Python Quickstart'


#PATHS
PROGRAM_DIR = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-2])
DATA_DIR = os.path.join(PROGRAM_DIR, 'data')
SRC_DIR = os.path.join(PROGRAM_DIR, 'src')
CREDENTIAL_DIR = os.path.join(os.path.expanduser('~'), '.credentials')
CREDENTIAL_PATH = os.path.join(CREDENTIAL_DIR, '.psync_user_credentials.json')
CLIENT_SECRET_DIR = os.path.join(os.path.expanduser('~'), '.psync_client_secrets.json')
CONFIG_FILE_NAME = 'config.json'
LOGIN_HTML_PATH = os.path.join(SRC_DIR, 'onlogin.html')


#ON GOOGLE DRIVE 
DRIVE_BASE_DIR = 'PenguinSync'
DRIVE_SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata'





#not currently in use
CONFIG_KEYS = ['base_folder_id']

