
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

target = '/home/piyushxdev/Ransomware-Detection-System'
for filename in os.listdir(target):
            print(filename)

# class Handler(FileSystemEventHandler):
#     # def on_any_event(self, event, target):
        

target = '/home/piyushxdev/Ransomware-Detection-System'
my_handler = Handler()


