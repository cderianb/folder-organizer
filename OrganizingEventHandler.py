import os
import glob
import time
import shutil
from watchdog.events import FileSystemEventHandler

#TODO: Add more soon!
ignore_exts = ['.tmp', '.crdownload']
docs_exts = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
img_exts = ['.jpg', '.png', '.jpeg']
compressed_exts = ['.zip']

class OrganizingEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.root = ''
        self.file_name = ''
        self.file_ext = ''
        self.event = ''

    def on_created(self, event):
        super().on_created(event)
        print(f"File created - {event.src_path}")
        
        if os.path.exists(event.src_path):
            self.handle_event(event)

    def on_deleted(self, event):
        # return super().on_deleted(event)
        ###
        #  TODO: after 30 days, moved to recycle bin
        # trus kasih notif di recycle bin selama 30hari baru permanen delete
        ###
        return NotImplementedError
    
    def on_modified(self, event):
        super().on_modified(event)
        print(f"File modified - {event.src_path}")

        if os.path.exists(event.src_path):
            self.handle_event(event)

    def handle_event(self, event):
        time.sleep(1) # wait 1 second for watchdog finishing the event creation
        
        self.event = event
        file_path, self.file_ext = os.path.splitext(self.event.src_path)
        print(f'now handling {self.event.src_path}')
        
        if self.file_ext in ignore_exts:
            print('ignored')
            return
        if len(self.file_ext.strip()) == 0:
            print(f'folder only')
            return # folder only
        if len((self.event.src_path.replace(f'{self.root}\\', '')).split('\\')) > 1:
            print(f'not handle {self.event.src_path}')
            return
        
        print('working')
        self.file_name = file_path.split('\\')[-1]

        if self.file_ext in docs_exts:
            self.move('documents')
        elif self.file_ext in img_exts:
            self.move('images')
        elif self.file_ext in compressed_exts:
            print(f'moving {self.event.src_path}')
            self.move('compresseds')
        else:
            self.move('others')

    def move(self, type:str):
        # check for target directory existence
        if not os.path.exists(f'{self.root}\\{type}'):
            os.makedirs(f'{self.root}\\{type}')

        #check if file with same name exist
        new_path = f'{self.root}\\{type}\\{self.file_name}{self.file_ext}'
        if os.path.exists(new_path):
            # count for duplicated file
            count = len(glob.glob(f'{self.root}\\{type}\\{self.file_name}*{self.file_ext}'))
            new_path = f'{self.root}\\{type}\\{self.file_name} ({count}) {self.file_ext}'
        print(f'moving {self.event.src_path} to {new_path}')
        shutil.move(self.event.src_path, new_path)

        #ganti jadi notif win10toast
        print(f'File moved to {type}')
        print('\n')