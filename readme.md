```
$ celery -A call_center worker -l info
```
```
$ celery -A call_center beat -l info
```
```
$ python call_center/watcher.py
```
```
$ python manage.py runserver
```