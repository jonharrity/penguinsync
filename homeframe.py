
import tkinter as tk
import webbrowser
import time

import constants
import driveids


#    TODO
#
# * make handle_sync_now thread safe


class HomeFrame(tk.Frame):
    
    
    
    def __init__(self, master, sync_server):
        tk.Frame.__init__(self, master)
    
        self.sync_server = sync_server
        
        self.create_widgets()
        
        
        
    
    # * - * - * - *
    # GUI CREATION
    # * - * - * - *

    
    
    def create_widgets(self):
        container = tk.Frame(self)

        title_panel = self.get_title_panel(container)
        sync_panel = self.get_sync_panel(container)
        auth_panel = self.get_auth_panel(container)
        
        title_panel.grid(row=0, column=0, padx=100, sticky=tk.N)
        sync_panel.grid(row=0, column=1, padx=100, sticky=tk.N)
        auth_panel.grid(row=0, column=2, padx=100, sticky=tk.N)
        
        container.pack()
        
        
    def get_title_panel(self, master):
        frame = tk.Frame(master)
        pady = 20
        
        title = tk.Label(frame, text='PenguinSync', font=('Arial', 22))
        title.grid(row=0, pady=pady)
        
        website_button = tk.Button(frame, text='open website', command=self.handle_open_website)
        website_button.grid(row=1, pady=pady)
        
        help_button = tk.Button(frame, text='open help page', command=self.handle_open_help)
        help_button.grid(row=2, pady=pady)
        
        return frame
        
        
    def get_sync_panel(self, master):
        frame = tk.Frame(master)
        pady = 20
        
        title = tk.Label(frame, text='Sync Details', font=('Arial', 18))
        title.grid(row=0, pady=pady)
        
        last_synced = tk.Label(frame, text=self.get_last_synced_text())
        last_synced.grid(row=1, pady=pady)
        self.label_last_synced = last_synced
        
        sync_now = tk.Button(frame, text='sync now', command=self.handle_sync_now)
        sync_now.grid(row=2, pady=pady)
        
        folder_name = tk.Label(frame, text='using folder on google drive:\n'+constants.DRIVE_BASE_DIR)
        folder_name.grid(row=3, pady=pady)
        
        files_synced = tk.Label(frame, text=self.get_files_synced_text())
        files_synced.grid(row=4, pady=pady)
        
        session_total = tk.Label(frame, text='session total upload size (MB):')
        session_total.grid(row=5, pady=pady)
        
        return frame
    
    
    def get_auth_panel(self, master):
        frame = tk.Frame(master)
        pady = 20
        
        title = tk.Label(frame, text='Auth Status', font=('Arial', 18))
        title.grid(row=0, pady=pady)
        
        internet_status = tk.Label(frame, text='Connected to internet:')
        internet_status.grid(row=1, pady=pady)
        
        login_status = tk.Label(frame, text='Logged in to google drive:')
        login_status.grid(row=2, pady=pady)
        
        try:
            if not self.is_logged_in:
                raise Exception()
        except:
                login_button = tk.Button(frame, text='login')
                login_button.grid(row=3)
                                
        return frame
    
    
    def get_last_synced_text(self):
        last_time = self.sync_server.last_synced_time
        if type(last_time) == time.struct_time: 
            time_text = time.strftime('%m/%d %I:%M%p', last_time)
        else:
            time_text = 'not yet this session'
        
        pre = 'last synced: '
        return pre + time_text
    
    def refresh_last_synced_label(self):
        self.label_last_synced['text'] = self.get_last_synced_text()
    
    
    def get_files_synced_text(self):
        count = len(driveids.DriveIds().keys())
        if not count: 
            count = 'none'
        
        pre = 'total files being synced: '
        return pre + str(count)
    
    def refresh_files_synced(self):
        self.label_files_synced['text'] = self.get_files_synced_text()
        
    
    # * - * - * - *
    # GUI EVENTS
    # * - * - * - *

    
    def handle_sync_now(self):
        self.sync_server.sync()
        
    def handle_open_website(self):
        url = 'https://github.com/jonharrity/penguinsync'
        webbrowser.open(url, 1)
        
    def handle_open_help(self):
        url = 'https://github.com/jonharrity/penguinsync'
        webbrowser.open(url, 1)
        
        
    # * - * - * - *
    # EVENT CALLBACKS
    # * - * - * - *

        
    def callback_finish_sync(self):
        self.refresh_last_synced_label()
        
        
        

    
    
    