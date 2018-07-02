import os
import time


def watchdog():
    os.system('python call_center/call_center/watcher.py')

if __name__ == '__main__':
    time.sleep(1)
    watchdog()
