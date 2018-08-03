
# Django-приложение для колл центра

## Приложение:
*  перехватывает активные звонки из asterisk и записывает их в базу данных
* получает информацию о звонках попавших на автоответчики записывает их в базу данных
* позволяет прослушать аудиозаписи разговоров и автоответчика 
* позволяет оператору добавить коментарий к звонку
* позволяет оператору переадресовать задачу исполнителю
* позволяет изменять статусы звонка
* ведет лог изменений задач пользователями

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
```
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


## Деплой:
1) Установить Ubuntu 16.04.

2) Установить git.
```
$ sudo apt-get install git
```
3) Установить docker и docker-compose.
```
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

$ sudo apt-key fingerprint 0EBFCD88

$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

$ sudo apt-get update

$ sudo apt-get install docker-ce

$ sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose
```
4) Скачивание и запуск приложение:
```
$ cd /path/to/progect

$ git clone "REPO"

$ cd /path/to/progect/docker

$ sudo docker-compose -f docker-compose_<регион>.yml up -d

``` 
## Обновление:

```
$ cd /path/to/progect/docker

$ sudo docker-compose -f docker-compose_<регион>.yml down --rmi all

$ git pull

$ sudo docker-compose -f docker-compose_<регион>.yml up -d
```

