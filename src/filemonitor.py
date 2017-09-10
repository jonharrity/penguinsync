import time
from threading import Thread

from watchdog.observers import Observer

from eventhandler import EventHandler


update_cloud_wait = 60 * 15# 60 seconds * 15 minutes

class FileMonitor(Thread):
    
    def __init__(self, gui_log, active_dirs):
        Thread.__init__(self)
        
        self.is_running = False
        
        global log
        log = gui_log

        
        self.active_dirs = active_dirs
        self.daemon = True
        
    
    def add_dir(self, new_dir):
        self.watches[new_dir] = self.observer.schedule(self.handler, new_dir, recursive=True)
        log("now monitoring directory %s " % new_dir)
        
        
        
    def remove_dir(self, old_dir):
        watch = self.watches.pop(old_dir)
        self.observer.unschedule(watch)
        log("removed directory from monitor " + old_dir)
        
        
    def run(self):
        
        self.watches = {}
        
        self.handler = handler = EventHandler(log)
        self.observer = observer = Observer()
        
        for path in self.active_dirs:
            self.watches[path] = observer.schedule(handler, path, recursive=True)
            
        observer.start()
        self.is_running = True
        

        try:
            while True:
                time.sleep(1)
        
        except:
            observer.stop()
            
        observer.join()
        
        
        
        
        