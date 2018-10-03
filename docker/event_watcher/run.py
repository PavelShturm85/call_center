import os
import time


def event_watch():
    os.system('python call_center/event_watcher.py')

if __name__ == '__main__':
    time.sleep(1)
    event_watch()

