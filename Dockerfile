FROM prefecthq/prefect:2.18-python3.12

COPY ./requirements.txt /rss_requirements.txt
COPY ./worker_run.sh /worker_run.sh

RUN pip3 install -r /rss_requirements.txt

CMD bash /worker_run.sh
