FROM python:3.8-slim-buster

RUN apt update && apt install -y ffmpeg git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000 8000

ENV GRADIO_SERVER_PORT 8000

COPY . .

CMD [ "python3", "app.py"]
