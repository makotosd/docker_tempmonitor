#
#
#
FROM ubuntu
#MAINTAINER takipone <xxxx@gmail.com>
RUN apt-get update -q -y && \
    apt-get upgrade -y && \
    apt-get install -y python-pip curl bc && \
    pip install wiringpi m2x line-bot-sdk
COPY get_temp.py /
COPY TempMonitor_M2X.sh /
COPY temperature_check_wrapper.py /
COPY check_temperature.py /

ENTRYPOINT [TempMonitor_M2X.sh]
