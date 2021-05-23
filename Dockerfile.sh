#!/usr/bin/env bash
docker build -t beeware - <<EOF
FROM debian:latest
RUN ln -s /src/home/.android /root
RUN ln -s /src/home/.briefcase /root
RUN ln -s /src/home/.kotlin /root
RUN ln -s /src/home/.gradle /root
RUN apt -y update
RUN apt -y install git python3-dev python3-venv libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkit2gtk-4.0-37 gir1.2-webkit2-4.0
RUN apt -y install python3-pip
RUN python3 -m pip install briefcase
EOF
