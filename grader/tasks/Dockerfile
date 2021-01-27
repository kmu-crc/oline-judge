FROM ubuntu:18.04
MAINTAINER sjhwang@cs.kookmin.com

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8
RUN update-locale LANG=ko_KR.UTF-8

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install python-ptrace

RUN apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/

RUN apt-get -y install g++

RUN pip install requests
RUN pip install numpy
RUN pip install redis

COPY grade_core /grade_core
COPY run_grade.py /
