
import httplib2
import hashlib
import os
import webbrowser

import constants

from apiclient import discovery
from oauth2client.file import Storage









def flow_for_credentials(service_callback):
    state = get_random_state()
    redirect_uri = constants.AUTH_SERVER_REDIRECT
    client_id = constants.AUTH_CLIENT_ID
    init_url = ( 'https://accounts.google.com/o/oauth2/v2/auth?' +
                ('scope=%s&' % constants.DRIVE_SCOPES) + 
                ('response_type=code&') + 
                ('state=%s&' % state) + 
                ('redirect_uri=%s&' % redirect_uri) + 
                ('client_id=%s' % client_id) )
    webbrowser.open(init_url, 1)



def request_drive_service(service_callback):
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








