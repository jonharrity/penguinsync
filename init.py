
import os

import tkinter as tk

import syncserver
import homeframe

START_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data"




def count_save_files():
    count = 0
    for file_name in ['adr', 'did', 'lsy']:
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



def main():
    
    if count_save_files() < 3:
        print("missing save files. remaking all.")
        create_save_files()
    
    
    sync_server = syncserver.SyncServer(START_DIR)
    print('completed: server init')
    
    frame = tk.Tk()
    home = homeframe.HomeFrame(frame, sync_server)
    home.pack()
    
    print('completed: homeframe init')
    frame.mainloop()



if __name__ == '__main__':
    main()
    
    
    