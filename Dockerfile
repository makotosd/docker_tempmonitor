#
#
#
FROM ubuntu
#MAINTAINER takipone <xxxx@gmail.com>
RUN apt-get update -q -y && \
    apt-get upgrade -y && \
    apt-get install -y python-pip curl ssmtp bc && \
    pip install wiringpi
COPY get_temp.py /
COPY TempMonitor_M2X.sh /
