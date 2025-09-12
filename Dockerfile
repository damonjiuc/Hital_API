FROM python:3.10

RUN mkdir /Hital_api

WORKDIR /hital_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /hital_api/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
