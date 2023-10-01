FROM python:3.10

WORKDIR /opt

RUN git clone https://github.com/tanovs/repka_project_backend.git

WORKDIR /opt/repka_project_backend

RUN git checkout develop
RUN git pull origin develop

RUN rm -rf nginx repka_admin docker_compose.yml

WORKDIR /opt/repka_project_backend/application

RUN apt-get update \
    && apt-get install -y netcat-traditional
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV POSTGRES_PASSWORD=123qwe
ENV POSTGRES_HOST=127.0.0.1
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB = repka_database
ENV POSTGRES_USER = repka
ENV MAIL_USERNAME = a.koreyba@repka.tech
ENV MAIL_PASSWORD=Shwg5qbtA9pDCDMG9vPZ
ENV MAIL_FROM=a.koreyba@repka.tech
ENV MAIL_PORT=587
ENV MAIL_SERVER=smtp.mail.ru
ENV MAIL_FROM_NAME="Repka tech API"


CMD ["python3.10", "main.py"]