
import tkinter as tk
from tkinter import ttk
import os

import syncserver
import homeframe
import explorerframe
import constants




"""
todo

    * in driveids, lastsynced and managedfolders, only save data when explicitly told to
        (currently saves anytime new entry is added or removed)




"""

def count_save_files():
    count = 0
    for file_name in ['did', 'lsy', 'msf']:
        path = constants.DATA_DIR + '/' + file_name
        if os.path.isfile(path):
            count += 1
    return count


def create_save_files():
    import pickle
    
    
    #drive_ids: dict
    did = open(constants.DATA_DIR + '/did', 'wb')
    pickle.dump({}, did)
    did.close()
    
    #last_synced: dict
    lsy = open(constants.DATA_DIR + '/lsy', 'wb')
    pickle.dump({}, lsy)
    lsy.close()

    #managed_subfolders: list
    msf = open(constants.DATA_DIR + '/msf', 'wb')
    pickle.dump([], msf)
    msf.close()


#callback to update explorerframe
def callback_finish_sync():
    global explorer
    explorer.refresh_all()



def main():
    
    gui_only = False
    enable_drive_service = True
    
    
    if count_save_files() < 3:
        print("missing save files. making all.")
        create_save_files()
    
    
    frame = tk.Tk()
    frame.wm_title("Penguin Sync")
    frame.tk_setPalette(background='#eff8f9')        

        
    if gui_only:
        explorerframe.ExplorerFrame(frame).pack()
        
        print('completed: homeframe init')
        frame.mainloop()
        
    else:
        global home, explorer
        
        
        sync_server = syncserver.SyncServer(constants.DATA_DIR, enable_drive_service=enable_drive_service)
        sync_server.register_on_sync(callback_finish_sync)
        
        ttk.Style().configure('TNotebook', background='#6fcbd6')
        notebook = ttk.Notebook(frame)
        
        home = homeframe.HomeFrame(notebook, sync_server)
        explorer = explorerframe.ExplorerFrame(notebook, sync_server)
        
        notebook.add(home, text="Home", sticky='nsew')
        notebook.add(explorer, text="Files")
        
        notebook.pack(fill=tk.BOTH, expand=1)
        
        
        sync_server.sync()
        
        frame.mainloop()



if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    