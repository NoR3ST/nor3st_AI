FROM nvidia/cuda:12.0.0-base-ubuntu20.04

RUN apt-get update -qq
RUN apt-get install ffmpeg -y
RUN apt-get install -y cmake
RUN apt-get install vim -y
RUN apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 3000