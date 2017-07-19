import tkinter as tk

import lastsynced, driveids, managedfolders

import time
import os


class FileFrame(tk.Frame):
    
    def __init__(self, master, syncserver):
        tk.Frame.__init__(self, master)
#         self['bd'] = 3
        self['relief'] = tk.GROOVE
        self.last_synced = lastsynced.LastSynced()
        self.drive_ids = driveids.DriveIds()
        self.managed_folders = managedfolders.ManagedFolders()
        self.base_path = '<All>'
        self.sync_server = syncserver
        
        self._tcl_counter = 0
        self.button_to_path = {}
        self.checkbutton_changes = []
        
        self.create_widgets()

    
    def get_title_text(self):
        if self.base_path == '<All>':
            return 'Displaying every synced file'
        else:
            return 'Displaying folder ' + self.base_path       
        
    def create_widgets(self):
#         button_container = tk.Frame(self)
#         tk.Button(button_container, text='Add Files', command=self.handle_add_files, 
#                 background='#b2eef4', font=8).grid(row=0, column=0, pady=20, sticky='W')
#         tk.Button(button_container, text='Remove Selected Files', command=self.handle_remove_files,
#                 background='#b2eef4', font=8).grid(row=0, column=1)
#         button_container.grid(row=0)

        side_frame = tk.Frame(self)
        tk.Label(side_frame, text='').grid(row=0, rowspan=2, padx=100, pady=80)
        tk.Checkbutton(side_frame, text='enable editing?').grid(row=2)
        tk.Button(side_frame, text='apply updates', command=self.apply_changes).grid(row=3)
        tk.Label(side_frame, text='updating statuses of:').grid(row=4)
        self.status_label = tk.Label(side_frame, text='')
        self.status_label.grid(row=5)
        
        side_frame.grid(row=0, column=0, rowspan=2)

        self.title = tk.Label(self, text=self.get_title_text(), font=5)
        self.title.grid(row=0, column=1)
        
        self.add_disposable_widgets()
        
        
        
    def apply_changes(self):        
        for path in self.checkbutton_changes:
            if not path in self.last_synced.keys():#add file
                self.sync_server.add_new_file(path)
            else:#remove file
                try:
                    self.last_synced.remove(path)
                    self.drive_ids.remove(path)
                except:
                    print('could not remove path ' + path)
        
        self.checkbutton_changes = []
        self.refresh_widgets()
        
        
    def get_status_text(self):
        return '\n'.join(self.checkbutton_changes)
        
        
        
    def get_display_files(self):
        if self.base_path == '<All>':
            for path in self.last_synced.keys():
                yield path
        else:
            for path in os.listdir(self.base_path):
                full_path = self.base_path + '/' + path
                if os.path.isfile(full_path):
                    yield full_path
        
    def add_disposable_widgets(self):
        self.container_frame = tk.Frame(self)
        
        padx = 20
        
        tk.Label(self.container_frame, text='syncing', font=4).grid(row=0, column=0, sticky='W', padx=padx)
        tk.Label(self.container_frame, text="files", font=4).grid(row=0, column=1, sticky='W')
        tk.Label(self.container_frame, text='last synced', font=4).grid(row=0, column=2, sticky='W', padx=padx)

        display_all = self.base_path == '<All>'

        i = 0
        self.button_to_path.clear()
        for path in self.get_display_files():
            i += 1
            new_var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.container_frame, variable=new_var)
            checkbutton.grid(row=i, sticky='W', padx=padx)
            if display_all or path in self.last_synced:
                checkbutton.select()
            else:
                checkbutton.deselect()
            new_var.trace('w', self.checkbutton_click)
            self.button_to_path[self.get_update_tcl_key()] = path

            tk.Label(self.container_frame, text=path).grid(row=i, column=1, sticky='W')
            if path in self.last_synced:
                tk.Label(self.container_frame, text=time.strftime('%m/%d %I:%M%p', 
                self.last_synced[path])).grid(row=i, column=2, sticky='W', padx=padx)
                    
        self.container_frame.grid(row=1, column=1, columnspan=2)
                
    #super hacky.. not good    
    def get_update_tcl_key(self):
        key = 'PY_VAR' + str(self._tcl_counter)
        self._tcl_counter += 1
        return key
                
    def checkbutton_click(self, a, b, c):
        path = self.button_to_path[a]
        if path in self.checkbutton_changes:
            self.checkbutton_changes.remove(path)
        else:
            self.checkbutton_changes.append(path)
            
        self.status_label['text'] = self.get_status_text()
    
                    
    def handle_folder_change(self, new_base):
        self.base_path = new_base
        self.checkbutton_changes = []
        self.refresh_widgets()
        
    def refresh_widgets(self):
        self.container_frame.destroy()
        self.add_disposable_widgets()
        self.status_label['text'] = self.get_status_text()

        
        
        
        
        
        
        
        
        
        
        