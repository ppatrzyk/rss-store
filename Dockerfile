FROM python:3.11.9

COPY ./requirements.txt /rss_requirements.txt
COPY ./worker_run.sh /worker_run.sh

RUN pip3 install -r /rss_requirements.txt

CMD bash /worker_run.sh
