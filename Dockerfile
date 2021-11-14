FROM python:3.9

WORKDIR /home

#ENV TELEGRAM_API_TOKEN=""
ENV DB_LOGIN="m1tr"
ENV DB_PASSWORD="39742Arte"
ENV DB_IP="192.168.0.246"
ENV DB_PORT="5432"
ENV DB_BASE="timtable_db"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY test_f/test_db.py .


ENTRYPOINT ["python", "test_db.py"]