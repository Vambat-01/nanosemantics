FROM python:3.9

COPY ./company_storage.py /app/company_storage.py
COPY ./server.py /app/server.py
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "server.py", "0.0.0.0", "8000", "postgres", "5432"]
