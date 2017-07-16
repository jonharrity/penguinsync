
import pickle
import constants


class ManagedFolders:
    
    def __init__(self):
        
        try:
            ManagedFolders.data
        except:
            ManagedFolders.data = self.load()
            
            
    def load(self):
        file = open(constants.START_DIR + "/msf", 'rb')
        managed_subfolders = pickle.load(file)
        file.close()
        return managed_subfolders   
     
    def save(self):
        file = open(constants.START_DIR + "/msf", 'wb')
        pickle.dump(ManagedFolders.data, file)
        file.close()
        
    def remove(self, path):
        ManagedFolders.data.remove(path)
        
    def clear(self):
        ManagedFolders.data.clear()
        self.save()
        
    def pop(self, index):
        ManagedFolders.data.pop(index)
        
    def append(self, newpath):
        ManagedFolders.data.append(newpath)
        self.save()
        
    def __contains__(self, path):
        return path in ManagedFolders.data
    
    def __len__(self):
        return len(ManagedFolders.data)
    
    def __getitem(self, path):
        return ManagedFolders.data[path]
    
    def __iter__(self):
        for path in ManagedFolders.data:
            yield path