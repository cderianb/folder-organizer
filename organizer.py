import sys
from OrganizingEventHandler import OrganizingEventHandler

from watchdog.observers import Observer

if __name__ == "__main__":
    #TODO: tambahin path ke suatu folder
    #TODO: tambahain initialize buat awal lgsg bersihin folder nya dulu
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = OrganizingEventHandler()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()