
import os
import sys

import tkinter as tk
from tkinter import ttk

import syncserver
import homeframe
import httplib2
import explorerframe

START_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data"




def count_save_files():
    count = 0
    for file_name in ['did', 'lsy', 'msf']:
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

    #managed_subfolders: list
    msf = open(START_DIR + '/msf', 'wb')
    pickle.dump([], msf)
    msf.close()


#callback to update explorerframe
def callback_finish_sync():
    global explorer
    explorer.refresh_all()
    home.update_sync_time()



def main():
    
    start_headless = False
    enable_drive_service = False
    
    
    if count_save_files() < 3:
        print("missing save files. making all.")
        create_save_files()
    
    
    frame = tk.Tk()
    frame.wm_title("Penguin Sync")
    frame.tk_setPalette(background='#eff8f9')
    
    
    if not start_headless:#normal mode:
        
        global home, explorer
        
        
        sync_server = syncserver.SyncServer(START_DIR, callback_finish_sync, enable_drive_service=enable_drive_service)
         
        notebook = ttk.Notebook(frame)
         
        home = homeframe.HomeFrame(notebook, sync_server)
        explorer = explorerframe.ExplorerFrame(notebook, sync_server)
         
        notebook.add(home, text="Home")
        notebook.add(explorer, text="Files")
         
        notebook.pack(fill=tk.BOTH, expand=1)
        
        frame.mainloop()
        
    else:#start headless
        
        

        explorerframe.ExplorerFrame(frame).pack()
        
        print('completed: homeframe init')
        frame.mainloop()



if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    