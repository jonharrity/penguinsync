from watchdog.events import FileSystemEventHandler




class EventHandler(FileSystemEventHandler):
    
    
    
    
    def __init__(self, gui_log):
        FileSystemEventHandler.__init__(self)
        
        global log
        log = gui_log
        
        
        
    def on_any_event(self, event):
        FileSystemEventHandler.on_any_event(self, event)
        
        if event.event_type is "modified" and event.is_directory:
            return
                
        message = event.event_type
        
        if event.is_directory:
            message += " dir "
        else:
            message += " file "
            
        message += event.src_path
        
        if event.event_type is "moved":
            message += " to %s" % event.dest_path
        


        log(message)
        
