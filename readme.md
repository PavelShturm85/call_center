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

### Команды для работы с докером.

sudo docker-compose -f docker-compose_<регион>.yml up -d
```
* создает контейнеры из конфигурационного файла и запускает их, без вывода лога в терминал.

```
sudo docker-compose -f docker-compose_<регион>.yml logs -f
```
* просмотр логов запущеных контейнеров.

```
sudo docker-compose -f docker-compose_<регион>.yml down --rmi all
```
* останавливает контейнеры и удаляет образы.

```
$ sudo docker-compose ps
```
* Просмотреть запущенные сервисы docker-compose

```
$ sudo docker-compose rm <id|name>
```
* удалить запущенные службы докер-компос
* --all - удаляет все службы

```
$ sudo docker image ls
```
* Показывает все имаджи в реестре компьютера

```
$ sudo docker container ls
```
* Показывает все запущенные контейнеры в реестре компьютера

```
$ sudo docker container rm <container name|id>
```
* Удаляет контейнер с указанным айди или неймом

```
$ sudo docker image rmi --force <image name|id>
```
* Удаляет имадж с указанным айди или неймом, вместе с контейнером

```
$ sudo docker exec -ti <id container> bash
```
* Зайти внутрь запущенного контейнера докера, через его id

```
$ docker run -ti -p <host_port>:<in_container_host> <container_name>
```
* Запускает контейнер с укзанным именем, привязывая порт компьютера к порту 
* внутри запущенного контейнера докера

