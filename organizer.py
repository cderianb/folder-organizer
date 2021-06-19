import os, sys, time
import winshell
import dateutil.parser
from winshell import ShellRecycledItem, recycle_bin
from OrganizingEventHandler import OrganizingEventHandler
from datetime import datetime
from send2trash import send2trash
from watchdog.observers import Observer

CURRENT_DATETIME = datetime.fromtimestamp(time.time())

def clean_folder(path):
    for folder, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(folder, file)
            last_used = datetime.fromtimestamp(os.path.getmtime(filepath))
            delta = CURRENT_DATETIME - last_used
            if delta.days >= 14:
                send2trash(filepath)

def clean_recycle_bin():
    deleted_files = list(winshell.recycle_bin())
    for deleted in deleted_files:
        recycled_date = (dateutil.parser.parse(str(deleted.recycle_date()))).replace(tzinfo=None)
        delta = CURRENT_DATETIME - recycled_date

#Kasih parameter absolute path folder yang mau di watch 
if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    #Clean folder from old files
    clean_folder(path)
    #clean_recycle_bin()

    #Watch realtime
    event_handler = OrganizingEventHandler()
    event_handler.root = path

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print(f'Organizer is now watching {path}')
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()