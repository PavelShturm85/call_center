FROM python:3.5-jessie

WORKDIR /crm

ADD . /crm
ADD /conf/local_settings/local_settings_64.py /crm/call_center/call_center/local_settings.py
ADD /event_watcher/event_watcher_64.py /crm/call_center/event_watcher.py

RUN apt-get update && apt-get upgrade -y && apt-get install -y  \
    --no-install-recommends apt-utils \
    build-essential libssl-dev libffi-dev python3-dev

RUN pip install -r requirements.txt

EXPOSE 3031

ENV NAME crm

CMD ["python", "docker/django/run.py"]
