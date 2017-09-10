import pickle
import constants


class DriveIds:
    
    
    def __init__(self):
        
        try:
            DriveIds.data
        except:
            DriveIds.data = self.load()
        
        
        
    def load(self):
        file = open(constants.DATA_DIR + "/did", 'rb')
        drive_ids = pickle.load(file)
        file.close()
        return drive_ids
        
    def save(self):
        file = open(constants.DATA_DIR + '/did', 'wb')
        pickle.dump(DriveIds.data, file)
        file.close()
        
    def __getitem__(self, path):
        return DriveIds.data[path]
    
    def __setitem__(self, path, val):
        DriveIds.data[path] = val
        self.save()
        
    def pop(self, path, arg):
        DriveIds.data.pop(path, arg)
        self.save()
        
    def keys(self):
        return DriveIds.data.keys()
    
    def clear(self):
        DriveIds.data.clear()
        self.save()
    
    
    