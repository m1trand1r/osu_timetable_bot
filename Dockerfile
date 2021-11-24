FROM python:3.9

WORKDIR /home

#ENV TELEGRAM_API_TOKEN=""
ENV DB_LOGIN=""
ENV DB_PASSWORD=""
ENV DB_IP=""
ENV DB_PORT=""
ENV DB_BASE=""

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY test_f/test_db.py .


ENTRYPOINT ["python", "test_db.py"]