FROM python:3.9

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .


ENTRYPOINT ["python", "server.py"]