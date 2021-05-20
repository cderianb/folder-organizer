import os
import glob
from watchdog.events import FileSystemEventHandler

#TODO: Add more soon!
docs_exts = ['.pdf', '.doc', '.docx']
img_exts = ['.jpg', 'png']
other_exts = ['.txt']
compressed_exts = ['.zip']

class OrganizingEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.file_ext = ''
        self.event = ''

    def on_created(self, event):
        super().on_created(event)

        self.event = event
        file_path, self.file_ext = os.path.splitext(self.event.src_path)

        #kalo len nya sudah >2 artinya file yang created sudah masuk ke dalam folder, ga usah di organize lagi
        if len(file_path.split('\\')) > 2: 
            return

        self.file_name = file_path.split('\\')[-1]

        if self.file_ext in other_exts:
            self.move('others')
        elif self.file_ext in docs_exts:
            self.move('documents')
        elif self.file_ext in img_exts:
            self.move('images')
        elif self.file_ext in compressed_exts:
            self.move('compresseds')

    def on_deleted(self, event):
        # return super().on_deleted(event)
        ###
        #  TODO: after 30 days, moved to recycle bin
        # trus kasih notif di recycle bin selama 30hari baru permanen delete
        ###
        return NotImplementedError

    def move(self, type:str):
        # check for target directory existence
        if not os.path.exists(type):
            os.makedirs(type)
        
        #check if file with same name exist
        new_path = f'{type}\\{self.file_name}{self.file_ext}'
        if os.path.exists(new_path):
            # hitung ada berapa file dengan nama itu
            count = len(glob.glob(f'{type}\\{self.file_name}*{self.file_ext}'))
            new_path = f'{type}\\{self.file_name} ({count}) {self.file_ext}'
        os.replace(self.event.src_path, new_path)
        
        #ganti jadi notif win10toast
        print(f'File moved to {type}')
        print('\n')