FROM ubuntu:18.04
MAINTAINER Ankit Solanki ankit03june@gmail.com

RUN apt-get update
RUN apt-get upgrade -y

RUN mkdir -p /myapp
WORKDIR /myapp
COPY . .

RUN apt-get install -y python python-setuptools python-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py --flask
