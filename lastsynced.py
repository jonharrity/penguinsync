import pickle
import constants



class LastSynced:
    
    
    def __init__(self):
        try:
            LastSynced.data
        except:
            LastSynced.data = self.load()
            
    def load(self):
        file = open(constants.START_DIR + "/lsy", 'rb')
        last_synced = pickle.load(file)
        file.close()
        return last_synced
    
    
    def save(self):
        file = open(constants.START_DIR + "/lsy", 'wb')
        pickle.dump(LastSynced.data, file)
        file.close()
        

    def __getitem__(self, path):
        return LastSynced.data[path]
    
    def __setitem__(self, path, val):
        LastSynced.data[path] = val
        self.save()
        
    def __contains__(self, path):
        return path in LastSynced.data
        
    def keys(self):
        return LastSynced.data.keys()
    
    def pop(self, path, arg):
        LastSynced.data.pop(path, arg)
        self.save()
        
    def clear(self):
        LastSynced.data.clear()
        self.save()
        
        
        
        