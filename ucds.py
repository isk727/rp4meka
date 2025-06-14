#!/usr/bin/env python3
import os
import sys
import socket
import sqlite3
import json
import configparser
config = configparser.ConfigParser()
config.read('/etc/mekapit/config')

def write_db(dg, ip):
    db = sqlite3.connect(config['DB']['DBNAME'], isolation_level=None)
    print(dg)
    dec = json.loads(dg)
    db.execute(config['DB']['SQL'], [dec['uuid'], dec['rid'], dg])
    db.close()

def main_unit():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(config['UDP']['PORT'])))
    while True:
        dg, ip = s.recvfrom(8192)
        write_db(dg, ip[0])

def daemonize():
#    pid = os.fork()#ここでプロセスをforkする
#    if pid > 0:#親プロセスの場合(pidは子プロセスのプロセスID)
#        pf = config['General']['PID_FILE'] + os.path.splitext(os.path.basename(__file__))[0] + '.pid'
#        pid_file = open(pf, 'w')
#        pid_file.write(str(pid)+"\n")
#        pid_file.close()
#        sys.exit()
#    if pid == 0:#子プロセスの場合
#        main_unit()
    main_unit()

if __name__ == '__main__':
    while True:
        daemonize()
