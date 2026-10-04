import time
import math
from collections import Counter 

SAFE_EXTENSIONS_TUPLE = (".zip", ".gz", ".png", ".jpg", ".pdf")
timestamps = []
file_entropies = {}

window_seconds = 30

def process_event(file, event_type):
    global timestamps
    t = time.time()
    cutoff = t - window_seconds
    timestamps.append(t)
    new_list = []
    for times in timestamps:
        if times > cutoff:
            new_list.append(times)
    timestamps = new_list

    rate = get_rate(timestamps)
    entropy = analyze_entropy(file) 

    Risk_Score = rate + entropy

    if Risk_Score == 0:
        return "Normal"

    if Risk_Score == 1:
        return "Suspicious"

    if Risk_Score == 2:
        return "Confirmed Threat"


def get_rate(timestamps):
    N = len(timestamps)
    T = 20
    if N > T:
        flag1 = 1
        return flag1
    else:
        flag1 = 0
        return flag1


def analyze_entropy(file):
    try:
        with open(file, "rb") as f:
                data = f.read()
    except (FileNotFoundError, PermissionError):
        return 0 
      
    if len(data) == 0:
        E = 0
        flag2 = 0
        return flag2
    
    else :
        counts = Counter(data)
        E = 0
        for c in counts.values():
            p = c/len(data)
            log = math.log2(p)
            E += p*log
        E = -E

        old_E = file_entropies.get(file, None)
        
        if old_E == None:
            file_entropies[file] = E
            if (E > 7.6) and file.lower().endswith(SAFE_EXTENSIONS_TUPLE):
                flag2 = 0
            else:
                flag2 = 1         
        else:
            delta_H = E - old_E
            if delta_H > 1.5:
                flag2 = 1
            else:
                flag2 = 0
           
        return flag2






    
