
# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-bullseye

WORKDIR /algolia-test

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]