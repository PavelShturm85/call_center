FROM python:3.5-jessie

WORKDIR /crm

ADD . /crm

RUN apt-get update && apt-get upgrade -y && apt-get install -y  \
    --no-install-recommends apt-utils \
    build-essential libssl-dev libffi-dev python3-dev

RUN pip install -r requirements.txt

ENV NAME celery_beat

CMD ["python", "docker/celery_beat/run.py"]
