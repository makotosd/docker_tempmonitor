#!/bin/sh
#
#
DEVICE_ID=7870230c081b7f4f678dde08bc7bcba7
PRIMARY_API_KEY=81faa53c80c0c084e797d706bc84be25
SQLDB=./temperature.db

#if [ ! -f $SQLDB ] ; then ./ArchiveDB.sh ; fi

if [ -f /proc/cpuinfo ] ; then
  grep "Hardware" /proc/cpuinfo > /dev/null
  if [ $? -eq 0 ] ; then
    temphumi=`python get_temp.py ${SQLDB}`
  else
    temphumi="25.0 25.0"
  fi
else
  temphumi="24.0 24.0"
fi
#temphumi=`python get_temp.py ${SQLDB}`
temp=`echo $temphumi | cut -d" " -f1`
humi=`echo $temphumi | cut -d" " -f2`

#./mailalert.sh $temp
#./mailalert2.sh $temp

curl --silent -i -X PUT http://api-m2x.att.com/v2/devices/${DEVICE_ID}/streams/temperature/value -H "X-M2X-KEY: ${PRIMARY_API_KEY}" -H "Content-Type: application/json" -d "{ \"value\": \"${temp}\" }" > /dev/null
curl --silent -i -X PUT http://api-m2x.att.com/v2/devices/${DEVICE_ID}/streams/humidity/value -H "X-M2X-KEY: ${PRIMARY_API_KEY}" -H "Content-Type: application/json" -d "{ \"value\": \"${humi}\" }" > /dev/null

python temperature_check_wrapper.py
