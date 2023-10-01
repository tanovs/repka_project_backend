FROM python:3.10

WORKDIR /opt

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y netcat-traditional
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3.10", "main.py"]