FROM dgladkov/snakepit:latest

RUN apt-get update && apt-get install -y python-pip netcat curl

COPY requirements.txt /requirements.txt
COPY requirements_dev.txt /requirements_dev.txt


COPY ./compose/python/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

RUN pip install -r /requirements.txt
RUN pip install -r /requirements_dev.txt

ENV LANG en_GB.UTF-8
ENV TEST_ES_SERVER=elasticsearch:9200

WORKDIR /app/src
ENTRYPOINT ["/entrypoint"]