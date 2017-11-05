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

AUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

AUTH_SERVER_BASE = 'https://fierce-bastion-75518.herokuapp.com'
AUTH_SERVER_BASE_SIMPLE = 'fierce-bastion-75518.herokuapp.com'
AUTH_SERVER_PUSH = AUTH_SERVER_BASE + '/push'
AUTH_SERVER_REDIRECT = AUTH_SERVER_BASE + '/cb'
AUTH_SERVER_POP = AUTH_SERVER_BASE + '/pop'

AUTH_CLIENT_ID = '402842006506-qv4bjdtjnfvb9i16llstd3cthfkkdhai.apps.googleusercontent.com'
USER_AGENT = 'PenguinSync/1.0 (+https://github.com/jonharrity/penguinsync)'





#SETTINGS
ENABLE_EXT_AUTH = True
















#not currently in use
CONFIG_KEYS = ['base_folder_id']


