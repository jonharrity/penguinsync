import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox

import managedfolders, driveids, lastsynced

import os


class FolderFrame(tk.Frame):
    
    def __init__(self, master, callback, syncserver=None):
        tk.Frame.__init__(self, master)
        self['bd'] = 3
        self.callback = callback
        self.sync_server = syncserver
        
        self.bttn_selected_bg = 'cyan'
        self.bttn_common_bg = 'white'
                        
        self.managed_folders = managedfolders.ManagedFolders()
        
        self.create_widgets()
        
    def on_click(self, event):
        widget = event.widget
        if self.currently_selected == widget:
            return
        
        self.set_selected(widget, True)
        self.set_selected(self.currently_selected, False)
        self.currently_selected = widget
        self.callback(widget['text'])

        
    def handle_add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path == () or folder_path == '':
            pass
        else:            
            add_all = msgbox.askyesno(title='Add folder ' + folder_path,
            message='Do you want to sync every file in this folder?')
            
            if self.sync_server == None:
                return
            self.sync_server.add_new_dir(folder_path, add_all)      
            self.refresh_widgets()
        
    def handle_remove_folder(self):
        folder = self.currently_selected['text']
        if folder == '<All>':
            remove_all = msgbox.askyesno(title='Remove every folder',
            message='Do you really want to remove every listed folder from sync?')
            
            if not remove_all:
                return
            
            self.managed_folders.clear()
            driveids.DriveIds().clear()
            lastsynced.LastSynced().clear()
            self.refresh_widgets()
            
        else:
            remove_folder = msgbox.askyesno(title='Remove folder ' + folder,
            message='Are you sure you want to remove\n%s\n and every file in it from being synced?' % folder)
            
            if not remove_folder:
                return
            
            do_ask_nested = False
            nested_folders = self.get_nested_folders(folder)
            if nested_folders:
                for nested_folder in nested_folders:
                    if nested_folder in self.managed_folders: 
                        do_ask_nested = True
                        break
            
            remove_nested = False
            if do_ask_nested:
                remove_nested = msgbox.askyesno(title='Remove contained folders',
                message='%s\ncontains folders that are marked for syncing. Do you ' +
                'want to remove those folders as well?')
            
            self.remove_files_in_folder(folder, remove_nested)
            self.refresh_widgets()
                
                
    def remove_files_in_folder(self, folder, remove_nested):
        self.managed_folders.remove(folder)
        drive_ids = driveids.DriveIds()
        last_synced = lastsynced.LastSynced()
        
        for name in os.listdir(folder):
            path = folder + '/' + name
            if os.path.isdir(path):
                if remove_nested and path in self.managed_folders:
                    self.remove_files_in_folder(path, remove_nested)
            else:
                drive_ids.pop(path)
                last_synced.pop(path)
            
        #remove nested folders not directly in folder
        if remove_nested:
            for managed_folder in self.managed_folders:
                if managed_folder[:len(folder)] == folder:
                    self.remove_files_in_folder(managed_folder, remove_nested)
            
            
        
        
    def set_selected(self, widget, selected):
        if not widget:
            return
        
        if selected:
            widget['background'] = self.bttn_selected_bg
        else:
            widget['background'] = self.bttn_common_bg
        
    
        
        
    def create_widgets(self):
        button_frame = tk.Frame(self)
        tk.Button(button_frame, text='Add folder', background='#b2eef4', font=8, 
                  command=self.handle_add_folder).grid(row=0, column=0, pady=20)
        tk.Button(button_frame, text='Remove selected folder', background='#b2eef4', font=8,
                  command=self.handle_remove_folder).grid(row=0, column=1)
        button_frame.grid(row=0)
        tk.Label(self, text='Folders', font=4).grid(row=1, sticky='W')
        self.add_disposable_widgets()
        
        
    def add_disposable_widgets(self):
        self.container_frame = tk.Frame(self)
            
        label = tk.Label(self.container_frame, text='<All>', bg=self.bttn_selected_bg)
        label.grid(row=0, column=0, sticky='W')
        label.bind("<Button-1>", self.on_click)
        self.currently_selected = label
        
        i = 0
        for path in self.managed_folders:
            i += 1
            label = tk.Label(self.container_frame, text=path, bg=self.bttn_common_bg)
            label.grid(row=i, column=0, sticky='W')
            label.bind("<Button-1>", self.on_click)
            
            
        
        self.container_frame.grid(row=2, sticky='W')
            
            
            
            
            
    def refresh_widgets(self):
        self.container_frame.destroy()
        self.add_disposable_widgets()
            
            
            
            
            
            
            