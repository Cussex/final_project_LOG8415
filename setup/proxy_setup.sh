#!/bin/bash -i

sudo apt-get update

sudo apt-get install python3 python3-pip -y

sudo pip3 install mysql-connector-python-rf
sudo pip3 install flask 
sudo pip3 install flask-restful
sudo pip3 install pythonping