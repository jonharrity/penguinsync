
import tkinter as tk


class ActiveFrame(tk.Frame):
    
    
    def __init__(self, master, sync_server):
        tk.Frame.__init__(self, master)
        
        self.selected = None
        self.listing = sync_server.active_dirs.copy()
        self.populate_list()
        
        
    def populate_list(self):
        for i in range(len(self.listing)):
            label = tk.Label(self, text=self.listing[i])
            label.grid(row=i, column=0)
            label.bind('<Button-1', self.on_click)
            
            
    def set_focus(self, widget):
        self.remove_focus(self.selected)
        
        if not self.selected == widget:
            widget['bg'] = '#55d68d'
            self.selected = widget
        
    def remove_focus(self, widget):
        if widget == None:
            return
        
        widget['bg'] = '#d9d9dd'
        self.selected = None
    
    
    def on_click(self, event):
        self.set_focus(event.widget)
        
        
    #returns the text of the selected
    def get_selected(self):
        if self.selected == None:
            return None
        else:
            return self.selected['text']