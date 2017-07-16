import tkinter as tk

from fileframe import FileFrame
from folderframe import FolderFrame

class ExplorerFrame(tk.Frame):
    
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        folderframe = FolderFrame(self, self.handle_folder_change)
        folderframe.grid(row=0, column=0, padx=50, sticky='N')

        self.fileframe = FileFrame(self)
        self.fileframe.grid_configure(row=0, column=1, padx=50)

#         self.columnconfigure(index=1, weight=2)
        
        
    def handle_folder_change(self, base):
        self.fileframe.handle_folder_change(base)
        
        
        
        