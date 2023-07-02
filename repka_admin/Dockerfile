FROM python:3.10

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y netcat
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV POSTGRES_PASSWORD=123qwe
# ENV POSTGRES_HOST=127.0.0.1
# ENV POSTGRES_PORT=5432
# ENV POSTGRES_NAME=repka_database
# ENV POSTGRES_USER=repka
# ENV SECRET_KEY='django-insecure-p0tnc=)(%lim3bb_*ye*k#!5azy-7wprk1u-akqj@(8au2!9f-'
# ENV DEBUG=True
# ENV ALLOWED_HOSTS=localhost,127.0.0.1

EXPOSE 8000

RUN chmod 777 start.sh

CMD ["bash", "start.sh"]