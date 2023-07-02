FROM python:3.10

WORKDIR /opt

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y netcat-traditional
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY uwsgi/uwsgi.ini application/uwsgi.ini

EXPOSE 8000

RUN chmod 777 start.sh

CMD ["bash", "start.sh"]