
import time

import tkinter as tk
from tkinter import messagebox 

import activeframe
from confirmdialog import ConfirmDialog

"""
todo

find a better name for last_synced_time so it isn't so close to last_synced

"""
class HomeFrame(tk.Frame):
    
    
    def __init__(self, master, sync_server):
        tk.Frame.__init__(self, master)
        self['bg'] = '#eff8f9'
        
        self.sync_server = sync_server
        
        self.add_widgets()
        
        self.start_sync_timer()
        
        
        
    def start_sync_timer(self):
        import threading
        minutes = 5
        seconds = minutes * 60
        threading.Timer(seconds, self.sync)
        
        
    def add_widgets(self):
        
        cloud_sync_label = tk.Label(self, text="Penguin Sync")
        cloud_sync_label['fg'] = 'blue'
        cloud_sync_label['font'] = ('Arial', 17)
        cloud_sync_label['pady'] = 30
        cloud_sync_label.grid(row=0)
        
        tk.Button(self, text='about').grid(row=1)
        tk.Button(self, text='preferences').grid(row=1, column=1, pady=20)
        
        self.sync_time_label = tk.Label(self)
        self.sync_time_label.grid(row=2, column=2, sticky='E')
        self.update_sync_time()
        self.sync_button = tk.Button(self, text='sync now', command=self.sync)
        self.sync_button.grid(row=3, column=2)
        
        tk.Label(self, text="<account_name>@gmail.com").grid(row=0, column=1)        
        
        
        tk.Label(self, text="Saving to drive folder Drive Client Storage").grid(row=3, pady=30)
#         tk.Label(self, text="Syncing every 5 minutes").grid(row=3, sticky='W')
        
        
        self.sync_list_frame = tk.Frame(self, pady=0)
        self.sync_list_frame['bg'] = '#d7f1f4'
        tk.Label(self.sync_list_frame, text="Syncing directories", bg='#d7f1f4').grid(row=0, column=0, sticky='W')
        tk.Button(self.sync_list_frame, text="add", command=self.add_active).grid(row=0, column=1)
        tk.Button(self.sync_list_frame, text="remove selected", command=self.remove_active).grid(row=0, column=2)
        
        self.sync_list_frame.grid(row=4)
        
        self.make_active_frame()

        
        
        
    def update_sync_time(self):
        last_time = self.sync_server.last_synced_time
        if type(last_time) == time.struct_time: 
            self.sync_time_label['text'] = ('last synced: ' + 
                    time.strftime('%m/%d %I:%M%p', 
                    last_time))
        else:
            self.sync_time_label['text'] = 'last synced:'
        
    def add_active(self, response=-1):
        if response == -1:
            ConfirmDialog(self, "Add new file or directory to sync", self.add_active)
            
        else:
            self.sync_server.add_new_active(response)
            self.active_frame.destroy()
            self.active_frame = activeframe.ActiveFrame(self, self.sync_server)

    def sync(self):
        self.sync_button['state'] = 'disabled'
        self.sync_server.sync()
        self.sync_button['state'] = 'normal'
        self.update_sync_time()
        
        self.start_sync_timer()
        
    def make_active_frame(self):
        self.active_frame = activeframe.ActiveFrame(self.sync_list_frame, self.sync_server)
        self.active_frame.grid(row=1, ipady=80)
        
    def remove_active(self):
        selected = self.active_frame.get_selected()
        if not selected:
            return
        
        confirm = messagebox.askyesno("Remove sync directory", 
                            "Confirm removing %s from active directories?"
                            % selected)
        
        if not confirm:
            return
        
        path = self.active_frame.get_selected()
        if path == None:
            return
        
        self.sync_server.remove_path_from_monitoring(path)
        self.active_frame.destroy()
        self.make_active_frame()
        
        
        
        
        
        