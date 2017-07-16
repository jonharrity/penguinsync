import tkinter as tk

import lastsynced
import time
import os


class FileFrame(tk.Frame):
    
    def __init__(self, master, syncserver=None):
        tk.Frame.__init__(self, master)
#         self['bd'] = 3
        self['relief'] = tk.GROOVE
        self.last_synced = lastsynced.LastSynced()
        self.base_path = '<All>'
        self.syncserver = syncserver
        
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

        self.title = tk.Label(self, text=self.get_title_text(), font=5)
        self.title.grid(row=0, pady=30)
        
        self.add_disposable_widgets()
        
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
        for path in self.get_display_files():
            i += 1
            checkbutton = tk.Checkbutton(self.container_frame)
            checkbutton.grid(row=i, sticky='W', padx=padx)
            if display_all or path in self.last_synced:
                checkbutton.select()
            else:
                checkbutton.deselect()
            tk.Label(self.container_frame, text=path).grid(row=i, column=1, sticky='W')
            if path in self.last_synced:
                tk.Label(self.container_frame, text=time.strftime('%m/%d %I:%M%p', 
                self.last_synced[path])).grid(row=i, column=2, sticky='W', padx=padx)
                    
        self.container_frame.grid(row=1, column=0, columnspan=2)
                
                
    def handle_folder_change(self, new_base):
        self.base_path = new_base
        self.title['text'] = self.get_title_text()
        self.refresh_widgets()
        
    def refresh_widgets(self):
        self.container_frame.destroy()
        self.add_disposable_widgets()
        
        
        
        
        
        
        
        
        
        
        
        