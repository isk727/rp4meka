#!/bin/bash
git='https://raw.githubusercontent.com/isk727/rp4meka/main/'
wget ${git}config.server
chmod 777 config.server
wget ${git}ucds.py
chmod 777 ucds.py
wget ${git}ucds.service
chmod 777 ucds.service
wget ${git}udpd.sql
chmod 777 udpd.sql
wget ${git}udpd.sqlite
chmod 777 udpd.sqlite
sudo mv config.server /etc/mekapit/config
sudo mv ucds.py /usr/share/ucds/ucds.py
sudo mv ucds.service /etc/systemd/system/ucds.service
sudo mv udpd.sql /usr/share/ucds/db/udpd.sql
sudo mv udpd.sqlite /usr/share/ucds/db/udpd.sqlite
echo 'Update is completed!'
