import os

import tkinter as tk

from confirmdialog import ConfirmDialog



class DirectoryListFrame(tk.Frame):
    
    
    
    def __init__(self, master, logger, get_active_dirs, set_active_dirs, file_monitor):
        tk.Frame.__init__(self, master)
        
        global log
        log = logger
        
        self.get_active_dirs = get_active_dirs
        self.set_active_dirs = set_active_dirs
        self.file_monitor = file_monitor

        
        self.create_widgets()
        
        
            
    def create_widgets(self):
        
        self.create_active_dirs_frame()
        
        self.create_exclude_dirs_frame()
        
        
    def create_active_dirs_frame(self):
        container = tk.Frame(self)
        container["background"] = "green"
        
        tk.Label(container, text="Monitor Directories").grid(row=0)
        
        add_button = tk.Button(container, text="add directory", command=self.add_dir)
        add_button.grid(row=1, column=0)
        
        remove_button = tk.Button(container, text="remove selected", command=self.remove_selected)
        remove_button.grid(row=1, column=1, padx=50)
        
        global listbox
        listbox = tk.Listbox(container)
        self.reset_listbox()
        listbox.grid(row=2, column=0, columnspan=2, pady=0, sticky="")
        
        container.grid(row=0, column=0, padx=50, ipady=100)
        
    def create_exclude_dirs_frame(self):
        pass
        
    def reset_listbox(self):
        listbox.delete(0, listbox.size()-1)
    
        for location in self.get_active_dirs():
            listbox.insert(tk.END, str(location))
            
            
    def get_selected_dirs(self):
        selected_indexes = listbox.curselection()
        selected_dirs = []
        for i in selected_indexes:
            selected_dirs.append(listbox.get(i))
        
        return selected_dirs
    
    
    def add_dir(self):
        message = "Add directory to list"
        ConfirmDialog(self, message, self.add_dir_callback)
        
    
    
    def add_dir_callback(self, callback_data, user_message):
        
        if user_message == "":
            return
        elif user_message in self.get_active_dirs():
            return
        
        new_dir = user_message
        if len(new_dir) < 1:
            return
        if not os.path.isdir(new_dir):
            log("%s is not a valid directory to add" % new_dir)
            return
        
        
        dirs = self.get_active_dirs()
        dirs.append(new_dir)
        
        self.set_active_dirs(dirs)
        
        self.reset_listbox()
        self.file_monitor.add_dir(new_dir)
        
    
        
    def confirm_removal(self, selected_list):
        confirm_message = "Confirm deleting the selected directories"
        
        for s in selected_list:
            confirm_message += "\n"
            confirm_message += s
            
        confirm_message += "\n"
        confirm_message += "\n"
        confirm_message += "by typing confirm:"
    
        ConfirmDialog(self, confirm_message, self.remove_selected_callback, selected_list)
    
    
    def remove_selected_callback(self, selected_dirs, user_message):
        user_message = str(user_message)
        confirm_key = "confirm"
        if user_message != confirm_key:
            return
    
    
        dirs = self.get_active_dirs()
        for single_dir in selected_dirs:
            dirs.remove(single_dir)
            self.file_monitor.remove_dir(single_dir)
    
        self.set_active_dirs(dirs)
        self.reset_listbox()
        
        
        
    def remove_selected(self):
    
        selected_dirs = self.get_selected_dirs()
        if len(selected_dirs) == 0:
            return
        
        self.confirm_removal(selected_dirs)
        
        
        
        
    