import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from tasks import SaveAnsweringMachineCalls
from django.conf import settings
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class Handler(FileSystemEventHandler):

    def on_created(self, event):
        path_to_file = event.src_path
        if path_to_file.split('.')[-1] != 'wav':
            save = SaveAnsweringMachineCalls(path_to_file)
            save.save_call()


observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, path=settings.MAIL_PATH_TO_ANSWERING_MACHINE, recursive=True)
observer.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
