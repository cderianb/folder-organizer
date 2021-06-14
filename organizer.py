import os, sys, stat
from OrganizingEventHandler import OrganizingEventHandler

from watchdog.observers import Observer

#Kasih parameter absolute path folder yang mau di watch 
if __name__ == "__main__":
    # C:\Users\Rained\Downloads
    #TODO: tambahin initialize buat awal lgsg bersihin folder nya dulu
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(path)
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
    except FileNotFoundError as e:
        with open('err.log', 'a') as f:
            f.write(e)
    observer.join()