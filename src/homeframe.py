
import tkinter as tk
import webbrowser
import time

import constants
import driveids


#    TODO
#
# * make handle_sync_now thread safe
#
# * change total upload size from bytes to a smart detection of bytes, kb, or mb




class HomeFrame(tk.Frame):
    
    
    
    def __init__(self, master, sync_server):
        tk.Frame.__init__(self, master)
    
        self.sync_server = sync_server
        self.is_logging_in = False
        
        self.create_widgets()
        
        sync_server.register_on_login(self.callback_login)
        sync_server.register_on_logout(self.callback_logout)
        sync_server.register_on_sync(self.callback_finish_sync)
        

    
    # * - * - * - *
    # GUI CREATION
    # * - * - * - *

    
    
    def create_widgets(self):
        container = tk.Frame(self)

        title_panel = self.get_title_panel(container)
        sync_panel = self.get_sync_panel(container)
        auth_panel = self.get_auth_panel(container)
        
        sync_panel.grid(row=0, column=0, padx=100, sticky=tk.N)
        title_panel.grid(row=0, column=1, padx=100, sticky=tk.N)
        auth_panel.grid(row=0, column=2, padx=100, sticky=tk.N)
        
        container.pack()
        
        
    def get_title_panel(self, master):
        frame = tk.Frame(master)
        pady = 20
        
        title = tk.Label(frame, text='PenguinSync', font=('Arial', 25))
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
        
        label_files_synced = tk.Label(frame, text=self.get_files_synced_text())
        label_files_synced.grid(row=4, pady=pady)
        self.label_files_synced = label_files_synced
        
        label_upload_total = tk.Label(frame, text=self.get_upload_total_text())
        label_upload_total.grid(row=5, pady=pady)
        self.label_upload_total = label_upload_total
        
        return frame
    
    
    def get_auth_panel(self, master):
        frame = tk.Frame(master)
        pady = 20
        
        title = tk.Label(frame, text='Auth Status', font=('Arial', 18))
        title.grid(row=0, pady=pady)
        
        label_internet_status = tk.Label(frame, text=self.get_connection_text())
        label_internet_status.grid(row=1, pady=pady)
        self.label_internet_status = label_internet_status
        
        label_login_status = tk.Label(frame, text=self.get_login_status_text())
        label_login_status.grid(row=2, pady=pady)
        self.label_login_status = label_login_status
        
        button_login = tk.Button(frame, text=self.get_login_button_text(), command=self.handle_login)
        button_login.grid(row=3, pady=pady)
        self.button_login = button_login
        
        
            
                                
        return frame
    
    
    # * - * - * - *
    # DYNAMIC LABELS
    # * - * - * - *
    
    
    def get_upload_total_text(self):
        bytes_total = self.sync_server.get_total_upload_size()
        #limit decimal length, but not integer length
#         mb = str(bytes_total / 10**6)
#         mb_left = mb.split('.')[0]
#         mb_right = mb.split('.')[1]
#         mb = mb_left + '.' + mb_right[:4]
        
        return 'session total upload size (bytes): ' + str(bytes_total)
    
    def refresh_upload_total_label(self):
        self.label_upload_total['text'] = self.get_upload_total_text()
    
    
    def get_login_status_text(self):
        if self.is_logging_in:
            return 'Logging in...'
        elif self.sync_server.is_logged_in():
            return 'Logged in to google drive'
        else:
            return 'Not logged in to google drive'
        
    def get_login_button_text(self):
        if self.is_logging_in:
            return 'Complete login'
        elif self.sync_server.is_logged_in():
            return 'logout'
        else:
            return 'login'
        
    def refresh_login_label_button(self):
        self.label_login_status['text'] = self.get_login_status_text()
        self.button_login['text'] = self.get_login_button_text()
            
    def get_connection_text(self):
        if self.sync_server.is_connected_to_internet():
            return 'Connected to the internet'
        else:
            return 'Not connected to the internet'
        
    def refresh_connection_label(self):
        self.label_internet_status['text'] = self.get_connection_text()
    
    
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
        
    def handle_login(self):
        if self.is_logging_in:
            self.sync_server.complete_login()
        elif self.sync_server.is_logged_in():
            self.sync_server.logout()
        else:
            self.sync_server.login()
            self.is_logging_in = True
            
        
        self.refresh_login_label_button()
        
        
        
    # * - * - * - *
    # EVENT CALLBACKS
    # * - * - * - *
    
    
    def callback_login(self):
        if self.is_logging_in:
            self.is_logging_in = False
        
        self.refresh_login_label_button()
    
    def callback_logout(self):
        self.refresh_login_label_button()

        
    def callback_finish_sync(self):
        self.refresh_last_synced_label()
        self.refresh_upload_total_label()
        self.refresh_connection_label()
        self.refresh_login_label_button()
        
        
        
    def callback_enable_finish_login(self):
        self.is_logging_in = True
        

    
    
    