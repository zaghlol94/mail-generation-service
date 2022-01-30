FROM python:3.9-slim

USER root


ENV APP_HOME /application
WORKDIR $APP_HOME
COPY . ./


RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html



RUN apt-get clean; \
    apt-get update; \
    apt-get -y upgrade; \
    apt install unzip
RUN bash download_model.bash
CMD  uvicorn app.main:app --host 0.0.0.0 --port $PORT
