
import httplib2
import hashlib
import os
import webbrowser

import constants
import authserver

from oauth2client.file import Storage
from oauth2client import client
from apiclient import discovery






def destroy_credentials():
    
    try:
        os.remove(constants.CREDENTIAL_PATH)
    except:
        pass
        
        
        
def request_credentials(service_callback):
    if not os.path.exists(constants.CREDENTIAL_DIR):
        os.makedirs(constants.CREDENTIAL_DIR)
        
    credentials = None
    credential_path = constants.CREDENTIAL_PATH
    if os.path.isfile(credential_path):
        store = Storage(credential_path)
        credentials = store.get()
        
    if not credentials or credentials.invalid:
        flow_for_credentials(service_callback)
    else:
        return_drive_service(credentials, service_callback)

def flow_for_credentials(service_callback):
    scope = constants.DRIVE_SCOPES
    secret_file = constants.CLIENT_SECRET_DIR
    redirect_port = 8000    
    redirect_uri = 'http://127.0.0.1:' + str(redirect_port)
    flow = client.flow_from_clientsecrets(secret_file, scope=scope, redirect_uri=redirect_uri)
    flow.user_agent = constants.APPLICATION_NAME

    tmp_server = authserver.AuthServer(redirect_port, flow_callback, (service_callback, flow))
    tmp_server.start_new_thread()

    auth_url = flow.step1_get_authorize_url()
    webbrowser.open(auth_url, 1)
    
def flow_callback(code, args):
    service_callback = args[0]
    flow = args[1]
    
    if not code:
        return_drive_service(None, service_callback)
        return
    
    credentials = flow.step2_exchange(code)
    return_drive_service(credentials, service_callback)
    
    
def request_drive_service(callback):
    credentials = request_credentials(callback)
    if credentials:
        return_drive_service(credentials, callback)
    
def return_drive_service(credentials, callback):
    if not credentials or credentials.invalid:
        callback(None)
        return

    store = Storage(constants.CREDENTIAL_PATH)
    store.put(credentials)
    
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)
    callback(drive_service)


def get_random_state():
    return hashlib.sha256(os.urandom(1024)).hexdigest()










