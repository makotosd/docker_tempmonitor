# -*- coding: utf-8 -*-
from m2x.client import M2XClient
import json
from linebot import LineBotApi
from linebot.models import TextSendMessage

TH_HI = 35
TH_LO = 22


def get_from_m2x():
    client = M2XClient(key='81faa53c80c0c084e797d706bc84be25')  # API-KEY

    device = client.device('7870230c081b7f4f678dde08bc7bcba7')  # DEVICE-ID
    #  client.devices()
    device.stream("temperature").values(limit=6)

    # Get raw HTTP response
    raw = client.last_response.raw

    # Get HTTP respose status code (e.g. `200`)
    status = client.last_response.status

    # Get HTTP response headers
    headers = client.last_response.headers

    # Get json data returned in HTTP response
    res_json = client.last_response.json
    values = res_json['values']

    return values


def label_for_values(values):
    zone = []
    for value in values:
        #  timestamp = value['timestamp']
        temperature = float(value['value'])

        if temperature > TH_HI:
            zone.append('TH_HI')
        elif temperature < TH_LO:
            zone.append('TH_LO')
        else:
            zone.append('NORMAL')
    return zone


def gen_message(labels, temperature):
    s = None

    count_hi = 0
    count_lo = 0
    count_no = 0
    for label in labels:
        if label is 'TH_HI':
            count_hi = count_hi + 1
        elif label is 'TH_LO':
            count_lo = count_lo + 1
        else:
            count_no = count_no + 1

    if count_hi is len(labels):
        #  全部温度が高い
        s = "temperature is too HOT!! {:.2f} degree!!".format(temperature)
    elif count_lo is len(labels):
        #  全部温度が低い
        s = "temperature is too LOW!! {:.2f} degree!!".format(temperature)
    else:
        if count_no is len(labels)-1 and labels[0] is 'TH_HI':
            #  NORMALから高温に変化
            s = "temperature is too HOT!! {:.2f} degree!!".format(temperature)
        elif count_no is len(labels)-1 and labels[0] is 'TH_LO':
            #  NORMALから低温に変化
            s = "temperature is too LOW!! {:.2f} degree!!".format(temperature)
        elif count_hi is len(labels)-1 and labels[0] is 'NORMAL':
            #  高温から常温に変化
            s = "temperature is return to normal. {:.2f} degree.".format(temperature)
        elif count_lo is len(labels)-1 and labels[0] is 'NORMAL':
            #  低温から常温に変化
            s = "temperature is return to normal. {:.2f} degree.".format(temperature)
        else:
            pass

    return s


def send_line_message(msg):
    ACCESS_TOKEN = 'ER+KnU1nE9Z1bDZ4dwNCz7INXVT+9zzFKt4RAzU2e/c2G0c9rB8EhcAFeHEbODRlVume3fQofmza9p+N6pdBP0cXiyNrO71bs89HV1S54X7234j+dGdukvhtBzgdCEv+Cf4VtpkVeIV8r1i0lC9gVQdB04t89/1O/w1cDnyilFU='
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=msg))

def check_temperature(test_file):
    #  m2xから値を取ってくる
    if test_file is None:
        values = get_from_m2x()
    else:
        f = open(test_file, 'r')
        values = json.load(f)

    #  値をもとに、range(TH_HI, NORMAL, TH_LO)をつける。
    labels = label_for_values(values)

    #  rangeをもとにメッセージを決める
    msg = gen_message(labels, values[0]['value'])

    #  LINEにmessageをpush
    if msg is not None:
        send_line_message(msg)


if __name__ == '__main__':
    #check_temperature('test04.json')  # no msg, hi/lo/no
    #check_temperature('test03.json')  # low -> nom
    #check_temperature('test02.json')  # hot -> nom
    check_temperature('test01.json')  # nom -> low
    #check_temperature('test00.json')  # nom -> hot

    check_temperature(None)
