# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /kindleDisplay


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/kindleDisplay

CMD [ "python3", "-m" , "flask", "--app", "run",  "run", "--host=0.0.0.0", "--port=5050"]
