FROM python:3.9.0-alpine3.12

ENV WORKING_DIRECTORY=/app

RUN mkdir $WORKING_DIRECTORY

WORKDIR $WORKING_DIRECTORY

COPY ./app.py app.py
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]