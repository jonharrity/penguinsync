
import httplib2
import hashlib
import os
import webbrowser
import http.client as http
import json

import constants

from apiclient import discovery
from oauth2client.client import OAuth2Credentials
from oauth2client.file import Storage

import google.oauth2.credentials as credmodule#@UnresolvedImport



"""
Notes:

Uses HTTPS connection. which
Requires python to be compiled with SSL support (through the ssl module)


"""



def destroy_credentials():
    
    try:
        os.remove(constants.CREDENTIAL_PATH)
    except:
        pass


def flow_for_credentials(service_callback):
    state = get_random_state()

    push_ext_server(state)
    open_auth_page(state)

    return state



def push_ext_server(state):
    conn = http.HTTPSConnection(constants.AUTH_SERVER_BASE_SIMPLE)  # @UndefinedVariable
    conn.request('GET','/push?state=' + state)
    response = conn.getresponse()
    data = response.read()
    print('after pushing to ext: received "%s"' % data)

def pop_ext_server(state, callback):
    conn = http.HTTPSConnection(constants.AUTH_SERVER_BASE_SIMPLE)  # @UndefinedVariable
    conn.request('GET', '/pop?state=' + state)
    response = conn.getresponse()
    data = response.read()
    print("popped ext server: data read is " + data)
    data = json.dumps(data)
    credentials = OAuth2Credentials(data['access_token'],
                    constants.AUTH_CLIENT_ID, '', data['refresh_token'],
                    data['expires_in'], constants.AUTH_TOKEN_URI,
                    constants.USER_AGENT)
    return_drive_service(credentials, callback)



def open_auth_page(state):
    redirect_uri = constants.AUTH_SERVER_REDIRECT
    client_id = constants.AUTH_CLIENT_ID
    init_url = (('https://accounts.google.com/o/oauth2/v2/auth?') +
                ('scope=%s&' % constants.DRIVE_SCOPES) +
                ('response_type=code&') +
                ('state=%s&' % state) +
                ('redirect_uri=%s&' % redirect_uri) +
                ('client_id=%s' % client_id) )
    webbrowser.open(init_url, 1)


#return state if flowing for credentials, otherwise returns None
def request_drive_service(service_callback, do_flow=True):
    credentials = load_credentials()

    if not credentials or credentials.invalid:
        return flow_for_credentials(service_callback)
    else:
        return_drive_service(credentials, service_callback)
        return None


#synchronous ; will NOT flow if no credentials
def get_service_from_file():
    credentials = load_credentials()
    if not credentials or credentials.invalid:
        return

    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    return drive_service


def load_credentials():
    if not os.path.exists(constants.CREDENTIAL_DIR):
        os.makedirs(constants.CREDENTIAL_DIR)

    credentials = None
    credential_path = constants.CREDENTIAL_PATH
    if os.path.isfile(credential_path):
        store = Storage(credential_path)
        credentials = store.get()

    return credentials


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








