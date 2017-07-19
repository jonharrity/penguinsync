import tkinter as tk

from fileframe import FileFrame
from folderframe import FolderFrame

class ExplorerFrame(tk.Frame):
    
    
    def __init__(self, master, syncserver=None):
        tk.Frame.__init__(self, master)
        
        self.folderframe = FolderFrame(self, self.handle_folder_change, syncserver)
        self.folderframe.grid(row=0, column=0, padx=50, sticky='N')

        self.fileframe = FileFrame(self, syncserver)
        self.fileframe.grid_configure(row=0, column=1, padx=50)

#         self.columnconfigure(index=1, weight=2)
        
        
    def handle_folder_change(self, base):
        self.fileframe.handle_folder_change(base)
        
        
        
    def refresh_all(self):
        self.folderframe.refresh_widgets()
        self.fileframe.refresh_widgets()
        
        
        