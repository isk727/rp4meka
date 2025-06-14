#!/usr/bin/env python3
import os
import sys
import time
import socket
import gpiozero
import json
import configparser
config = configparser.ConfigParser()
config.read('/etc/mekapit/config')

lEnable = gpiozero.LED(int(config['GPIO']['ENABLE']))
lBet = gpiozero.PWMLED(int(config['GPIO']['BET']))
lStart = gpiozero.PWMLED(int(config['GPIO']['START']))
lStop1 = gpiozero.PWMLED(int(config['GPIO']['STOP1']))
lStop2 = gpiozero.PWMLED(int(config['GPIO']['STOP2']))
lStop3 = gpiozero.PWMLED(int(config['GPIO']['STOP3']))
lAuto = gpiozero.LED(int(config['GPIO']['AUTO']))

def send_gpio(dgram):
    dg = json.loads(dgram)
    print(dg)
    pin = int(dg['pin'])
    num = int(dg['num'])
    if pin == int(config['GPIO']['ENABLE']):
        lEnable.value = num # enable
    elif pin == int(config['GPIO']['BET']):
        lBet.pulse() # bet
    elif pin == int(config['GPIO']['START']):
        lStart.pulse() # start
    elif pin == int(config['GPIO']['STOP1']):
        lStop1.pulse() # stop1
    elif pin == int(config['GPIO']['STOP2']):
        lStop2.pulse() # stop2
    elif pin == int(config['GPIO']['STOP3']):
        lStop3.pulse() # stop3
    elif pin == int(config['GPIO']['AUTO']):
        lAuto.value = num # auto
    else:
        btn = gpiozero.Button(int(dg['pin']))

def main_unit():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(config['UDP']['PORT'])))
    while True:
        dgram, addr = s.recvfrom(8192)
        if addr[0] == int(config['UDP']['IP_ADDRESS']):
            send_gpio(dgram)

def daemonize():
#    pid = os.fork() #ここでプロセスをforkする
#    if pid > 0: #親プロセスの場合(pidは子プロセスのプロセスID)
#        pf = config['General']['PID_FILE'] + os.path.splitext(os.path.basename(__file__))[0] + '.pid'
#        pid_file = open(pf, 'w')
#        pid_file.write(str(pid)+"\n")
#        pid_file.close()
#        sys.exit()
#    if pid == 0: #子プロセスの場合
#        main_unit()
    main_unit()

if __name__ == '__main__':
    while True:
        daemonize()
