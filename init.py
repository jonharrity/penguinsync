
import os
import sys

import tkinter as tk

import syncserver
import homeframe
import httplib2

START_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data"




def count_save_files():
    count = 0
    for file_name in ['adr', 'did', 'lsy', 'msf']:
        path = START_DIR + '/' + file_name
        if os.path.isfile(path):
            count += 1
    return count


def create_save_files():
    import pickle
    
    
    #drive_ids: dict
    did = open(START_DIR + '/did', 'wb')
    pickle.dump({}, did)
    did.close()
    
    #last_synced: dict
    lsy = open(START_DIR + '/lsy', 'wb')
    pickle.dump({}, lsy)
    lsy.close()
    
    #active_dirs: list
    adr = open(START_DIR + '/adr', 'wb')
    pickle.dump([], adr)
    adr.close()
    
    #managed_subfolders: list
    msf = open(START_DIR + '/msf', 'wb')
    pickle.dump([], msf)
    msf.close()



def main():
    
    if count_save_files() < 4:
        print("missing save files. remaking all.")
        create_save_files()
            
    try:
        sync_server = syncserver.SyncServer(START_DIR)
    except httplib2.ServerNotFoundError:
        print("unable to connect to server. exiting")
        sys.exit()
        
    
    print('completed: server init')
    
    frame = tk.Tk()
    home = homeframe.HomeFrame(frame, sync_server)
    home.pack()
    
    print('completed: homeframe init')
    frame.mainloop()



if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    