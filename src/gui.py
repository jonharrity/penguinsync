import pickle
import time
import os 

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


from filemonitor import FileMonitor

from directorylistframe import DirectoryListFrame



start_dir = os.path.dirname(os.path.realpath(__file__)) + "/data"
active_dirs = []

# def add_dir():
#     message = "Add directory to list"
#     ConfirmDialog(frame, message, add_dir_callback)
#     
# 
# 
# def add_dir_callback(callback_data, user_message):
#     
#     if user_message == "":
#         return
#     elif user_message in active_dirs:
#         return
#     
#     new_dir = user_message
#     if len(new_dir) < 1:
#         return
#     if not os.path.isdir(new_dir):
#         log("%s is not a valid directory to add" % new_dir)
#         return
#     
#     active_dirs.append(new_dir)
#     save_active_dirs()
#     reset_listbox()
#     file_monitor.add_dir(new_dir)

    
def reset_listbox():
    directory_list_frame.reset_listbox()
        
def get_active_dirs():
    return active_dirs

def set_active_dirs(new_dirs):
    active_dirs = new_dirs
    save_active_dirs()


def get_save_file_path():
    return start_dir + "/adr"


def load_active_dirs():
    try:
        global active_dirs
        
        save_file = open(get_save_file_path(), 'rb')
        active_dirs = pickle.load(save_file)
        save_file.close()
    
    except:
        pass
        
    
    
def save_active_dirs():
    try:
        save_file = open(get_save_file_path(), "wb")
        pickle.dump(active_dirs, save_file)
        save_file.close()
        
    except:
        pass
    
    
# def confirm_removal(selected_list):
#     confirm_message = "Confirm deleting the selected directories"
#     
#     for s in selected_list:
#         confirm_message += "\n"
#         confirm_message += s
#         
#     confirm_message += "\n"
#     confirm_message += "\n"
#     confirm_message += "by typing confirm:"
# 
#     ConfirmDialog(frame, confirm_message, remove_selected_callback, selected_list)
# 
# 
# def remove_selected_callback(selected_dirs, user_message):
#     user_message = str(user_message)
#     confirm_key = "confirm"
#     if user_message != confirm_key:
#         return
# 
# 
#     for single_dir in selected_dirs:
#         active_dirs.remove(single_dir)
#         file_monitor.remove_dir(single_dir)
# 
#     save_active_dirs()
#     reset_listbox()
# 
#     
#     
#     
# def remove_selected():
# 
#     selected_dirs = directory_list_frame.get_selected_dirs()
#     if len(selected_dirs) == 0:
#         return
#     
#     confirm_removal(selected_dirs)



def log(note):
    timeformat = "%m/%d %I:%M:%S"
    timestamp = time.strftime(timeformat)
    
    entry = timestamp + "   " + str(note) + "\n"
    
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, entry)
    log_text.config(state=tk.DISABLED)



def create_widgets():
    
    
    nb = ttk.Notebook(frame)
    
    global directory_list_frame
    directory_list_frame = DirectoryListFrame(frame, log, get_active_dirs, set_active_dirs, file_monitor)
#     directory_list_frame.grid(row=0, column=0) 
#     nb.add(directory_list_frame, "Directory Listing")
    nb.add(directory_list_frame, text="Directory Lists")

    global log_text
#     log_text = tk.Text(frame)
    log_text = ScrolledText(frame)
    log_text.config(state=tk.DISABLED)
#     log_text.grid(row=0, column=1)
    nb.add(log_text, text="Log")

    nb.pack(expand=1, fill="both")

def create_gui():
    load_active_dirs()
    
    global file_monitor
    file_monitor = FileMonitor(log, active_dirs)
    
    global frame
    frame = tk.Tk()
    create_widgets()
    

    file_monitor.start()
    
    log("Started application.")
    log("serving directories %s" % str(active_dirs))
    frame.mainloop()
    






if __name__ == "__main__":
    create_gui()
    
    
    
    
    