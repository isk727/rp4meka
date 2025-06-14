#!/bin/bash
git='https://raw.githubusercontent.com/isk727/rp4meka/main/'
wget ${git}config.rp
chmod 777 config.rp
wget ${git}gpiopi.py
chmod 777 gpiopi.py
wget ${git}gpiopi.service
chmod 777 gpiopi.service
wget ${git}ucdr.py
chmod 777 ucdr.py
wget ${git}ucdr.service
chmod 777 ucdr.service
sudo mv config.rp /etc/mekapit/config
sudo mv gpiopi.py /usr/share/gpiopi/gpiopi.py
sudo mv gpiopi.service /etc/systemd/system/gpiopi.service
sudo mv ucdr.py /usr/share/ucdr/ucdr.py
sudo mv ucdr.service /etc/systemd/system/ucdr.service
echo 'Update is completed!'
