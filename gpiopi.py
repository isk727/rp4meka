#!/usr/bin/env python3
import os
import sys
import time
import socket
import json
import uuid
import RPi.GPIO as GPIO
import configparser
config = configparser.ConfigParser()
config.read('/etc/mekapit/config')

# #####################################
# setup
# #####################################
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in range(16):
        GPIO.setup(i + 2, GPIO.OUT)
    for i in range(8):
        GPIO.setup(i + 20, GPIO.IN)
        GPIO.setup(i + 20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for i in range(16):
        GPIO.output(i + 2, 0)
    GPIO.add_event_detect(int(config['GPIO']['CREDIT_DEC']), GPIO.RISING, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['CREDIT_DEC']), event_callback_credit_dec)
    GPIO.add_event_detect(int(config['GPIO']['CREDIT_INC']), GPIO.RISING, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['CREDIT_INC']), event_callback_credit_inc)

    GPIO.add_event_detect(int(config['GPIO']['STATUS_AP']), GPIO.BOTH, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['STATUS_AP']), event_callback_status_ap)
    GPIO.add_event_detect(int(config['GPIO']['STATUS_RB']), GPIO.BOTH, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['STATUS_RB']), event_callback_status_rb)
    GPIO.add_event_detect(int(config['GPIO']['STATUS_BB']), GPIO.BOTH, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['STATUS_BB']), event_callback_status_bb)
    GPIO.add_event_detect(int(config['GPIO']['STATUS_CT']), GPIO.BOTH, bouncetime=5)
    GPIO.add_event_callback(int(config['GPIO']['STATUS_CT']), event_callback_status_ct)
    print('setup done')

# #####################################
# destroy
# #####################################
def destroy():
    GPIO.remove_event_detect(int(config['GPIO']['CREDIT_DEC']))
    GPIO.remove_event_detect(int(config['GPIO']['CREDIT_INC']))
    GPIO.remove_event_detect(int(config['GPIO']['STATUS_AP']))
    GPIO.remove_event_detect(int(config['GPIO']['STATUS_RB']))
    GPIO.remove_event_detect(int(config['GPIO']['STATUS_BB']))
    GPIO.remove_event_detect(int(config['GPIO']['STATUS_CT']))
    GPIO.cleanup()

# #####################################
# main loop
# #####################################
def main_unit():
    setup()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(config['UDP']['PORT'])))
    while True:
        datagram, address = s.recvfrom(8192)

# #####################################
# イベント：クレジット減算
# #####################################
def event_callback_credit_dec(gpio_pin):
    sendUDP('CREDIT', 0)

# #####################################
# イベント：クレジット加算
# #####################################
def event_callback_credit_inc(gpio_pin):
    sendUDP('CREDIT', 1)

# #####################################
# イベント：オートプレイ
# #####################################
def event_callback_status_ap(gpio_pin):
    sendUDP('AP', 1)

# #####################################
# イベント：レギュラーボーナス
# #####################################
def event_callback_status_rb(gpio_pin):
    sendUDP('RB', 0)

# #####################################
# イベント：ビッグボーナス
# #####################################
def event_callback_status_bb(gpio_pin):
    sendUDP('BB', 0)

# #####################################
# イベント：
# #####################################
def event_callback_status_ct(gpio_pin):
    sendUDP('CT', 0)

# #####################################
# サーバーへUDP送信
# #####################################
def sendUDP(cmd, val):
    data = {'uuid': str(uuid.uuid4()), 'rid': config['General']['RID'], 'command': str(cmd), 'value': val}
    json_data = json.dumps(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(json_data.encode(), (config['UDP']['IP_ADDRESS'], int(config['UDP']['PORT'])))
    s.close()

def daemonize():
    pid = os.fork()
    if pid > 0:
        pf = config['General']['PID_FILE'] + os.path.splitext(os.path.basename(__file__))[0] + '.pid'
        pid_file = open(pf, 'w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        main_unit()
#    main_unit()

if __name__ == '__main__':
    while True:
        daemonize()
