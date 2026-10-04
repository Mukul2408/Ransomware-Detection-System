import risk_analyzer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        file = event.src_path
        risk_analyzer.process_event(file)
