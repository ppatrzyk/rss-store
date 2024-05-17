FROM python:3.11.9

COPY ./requirements.txt /requirements.txt
COPY ./worker_run.sh /worker_run.sh

RUN pip3 install -r /requirements.txt

CMD bash /worker_run.sh
