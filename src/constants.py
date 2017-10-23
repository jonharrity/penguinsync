import os


APPLICATION_NAME = 'Penguin Sync'


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

AUTH_SERVER_BASE = ''
AUTH_SERVER_PUSH = AUTH_SERVER_BASE + '/push'
AUTH_SERVER_REDIRECT = AUTH_SERVER_BASE + '/cb'
AUTH_SERVER_POP = AUTH_SERVER_BASE + '/pop'

AUTH_CLIENT_ID = '402842006506-q8qjida6ob94156d7dv33r5l00n69c85.apps.googleusercontent.com'


#not currently in use
CONFIG_KEYS = ['base_folder_id']

