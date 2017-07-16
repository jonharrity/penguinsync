
import time


class TimeCompare:
    
    
    """
    stamp type:
        sse: seconds since epoch
        rfc3339: google rest api standard
    """    
    def __init__(self, timestamp, stamp_type):    
        
        if stamp_type == 'sse':
            self.stamp = time.localtime(timestamp)
        elif stamp_type == 'rfc3339':
            self.stamp = time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            raise Exception("Invalid time type provided: %s" % stamp_type)
        
    """
    other must be of type TimeCompare
    Returns difference in seconds between this instance and other
    positive if self time is after other, negative if self time is before other, 
    0 if they are the same time
    """
    def compare(self, other):
        if not isinstance(other, TimeCompare):
            raise Exception("%s is invalid type for method TimeCompare.compare" % type(other))
        
        return self.stamp.mktime() - other.stamp.mktime()
    
    """
    True if this instance comes before other,
    false otherwise
    """
    def comes_before(self, other):
        return self.compare(other) < 0
    
    def comes_after(self, other):
        return self.compare(other) > 0