import time
import math
from collections import Counter 
import os

SAFE_EXTENSIONS_TUPLE = (".zip", ".gz", ".png", ".jpg", ".pdf", ".jpeg", ".gif", ".webp", ".docx", ".xlsx", ".pptx", ".mp3", ".mp4", ".7z", ".rar")
timestamps = []
file_entropies = {}
max_risk_score = 0
window_seconds = 30

def process_event(file, prev_file = None, is_deleted = None):
    global timestamps, max_risk_score

    if is_deleted:
        file = os.path.normpath(file)
        file_entropies.pop(file, None)
        if max_risk_score == 2:
            return "Confirmed Threat"
        if max_risk_score == 1:
            return "Suspicious"
        return "Normal"
    
    t = time.time()
    cutoff = t - window_seconds
    timestamps.append(t)
    new_list = []
    for times in timestamps:
        if times > cutoff:
            new_list.append(times)
    timestamps = new_list

    rate = get_rate(timestamps)
    entropy = analyze_entropy(file, prev_file) 

    Risk_Score = rate + entropy
    if Risk_Score > max_risk_score:
        max_risk_score = Risk_Score
    if max_risk_score == 0:
        return "Normal"
    if max_risk_score == 1:
        return "Suspicious"
    if max_risk_score == 2:
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


def analyze_entropy(file, prev_file = None):
    try:
        with open(file, "rb") as f:
                data = f.read()
    except OSError:
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

        old_E = None
        if prev_file and prev_file in file_entropies:
            old_E = file_entropies.pop(prev_file)
        else:
            old_E = file_entropies.get(file, None)
        
        if old_E == None:
            file_entropies[file] = E
            if (E > 7.0) and not file.lower().endswith(SAFE_EXTENSIONS_TUPLE):
                flag2 = 1
            else:
                flag2 = 0        
        else:
            delta_H = E - old_E
            if delta_H > 1.5:
                flag2 = 1
            else:
                flag2 = 0

        file_entropies[file] = E           
        return flag2

def reset():
    global timestamps, max_risk_score
    timestamps = []
    max_risk_scores = 0
    file_entropies.clear()

def scan_baseline(folder):
    for root_dir, dirs, files in os.walk(folder):
        for name in files:
            path = os.path.normpath(os.path.join(root_dir, name))
            try:
                with open(path, "rb") as f:
                    data = f.read()
            except OSError:
                continue
            if len(data) > 0:
                counts = Counter(data)
                E = 0
                for c in counts.values():
                    p = c / len(data)
                    log = math.log2(p)
                    E += p * log
                E = -E
                file_entropies[path] = E






    
