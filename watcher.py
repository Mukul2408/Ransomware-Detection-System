from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shared
import risk_analyzer


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return 
        state=(risk_analyzer.process_event(event.src_path)
               if shared.scanner_active
               else "Disabled"
        )
        shared.events.put(("File Created", event.src_path, state))
    def on_modified(self, event):
        if event.is_directory:
            return
        state=(risk_analyzer.process_event(event.src_path)
                if shared.scanner_active
                else "Disabled"
        )
        shared.events.put(("File Modified", event.src_path,state))
    def on_moved(self, event):
        if event.is_directory:
            return
        state=(risk_analyzer.process_event(event.dest_path, prev_file = event.src_path)
                if shared.scanner_active
                else "Disabled"
        )
        shared.events.put(("File Moved", event.dest_path,state))
    def on_deleted(self, event):
        if event.is_directory:
            return
        state=(risk_analyzer.process_event(event.src_path, is_deleted = True)
                if shared.scanner_active
                else "Disabled"
        )
        shared.events.put(("File Deleted", event.src_path,state))
def start_watcher(folder):
    risk_analyzer.reset()
    risk_analyzer.scan_baseline(folder)
    obs=Observer()
    obs.schedule(Handler(),folder,recursive=True)
    obs.start()
    return obs
def stop_watcher(obs):
    if obs is not None:
        obs.stop()
        obs.join()


