FROM python:3.8-slim-buster

RUN apt update && apt install -y ffmpeg

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV GRADIO_SERVER_PORT 8000

COPY . .

CMD [ "python3", "app.py"]
