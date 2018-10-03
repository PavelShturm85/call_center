import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'call_center.settings')
django.setup()
import time
from call_center.tasks import SaveAnsweringMachineCalls
from django.conf import settings
import inotify.adapters


def _watcher():
    i = inotify.adapters.Inotify()

    i.add_watch(settings.MAIL_PATH_TO_ANSWERING_MACHINE)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if type_names[0] == 'IN_MOVED_TO' and filename.split('.')[-1] == 'txt':
            path_to_file = os.path.join(path, filename)
            save = SaveAnsweringMachineCalls(path_to_file)
            save.save_call()


if __name__ == '__main__':
    _watcher()
