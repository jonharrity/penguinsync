
import tkinter as tk
from tkinter import messagebox

import activeframe
from confirmdialog import ConfirmDialog

"""
todo




"""
class HomeFrame(tk.Frame):
    
    
    def __init__(self, master, sync_server):
        tk.Frame.__init__(self, master)
        
        self.sync_server = sync_server
        
        self.add_widgets()
        
        
        
    def add_widgets(self):
        
        tk.Label(self, text="Google account: <account_name>").grid(row=0, sticky='W')
        tk.Label(self).grid(row=1)
        
        tk.Label(self, text="Saving to drive folder Drive Client Storage").grid(row=2, sticky='W')
        tk.Label(self, text="Syncing every 5 minutes").grid(row=3, sticky='W')
        tk.Label(self).grid(row=4)
        
        tk.Label(self, text="Syncing directories").grid(row=5, column=0, sticky='W')
        tk.Button(self, text="add", command=self.add_active).grid(row=5, column=1)
        tk.Button(self, text="remove selected", command=self.remove_active).grid(row=5, column=2)
        
        self.active_frame = activeframe.ActiveFrame(self, self.sync_server)
        self.active_frame.grid(row=6, ipady=80)
        
        
    def add_active(self, response=-1):
        if response == -1:
            ConfirmDialog(self, "Add new file or directory to sync", self.add_active)
            
        else:
            self.sync_server.add_new_active(response)
            self.active_frame.destroy()
            self.active_frame = activeframe.ActiveFrame(self.sync_server)

        
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
        self.active_frame = activeframe.ActiveFrame(self.sync_server)
        
        
        
        
        
        
        
        