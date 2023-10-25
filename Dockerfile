FROM nvidia/cuda:12.0.0-base-ubuntu20.04

RUN apt-get update -qq && \
    apt-get install -y ffmpeg cmake vim software-properties-common curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt-get install -y python3.11

# Upgrade pip for Python 3.11
RUN apt install python3.11 
RUN apt install -y python3-pip
RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY . .

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt