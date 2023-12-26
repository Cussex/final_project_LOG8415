#!/bin/bash -i

sudo apt-get update

# Install Python3 and pip3
sudo apt-get install python3 python3-pip -y

# Install Flask and Flask-RESTful
sudo pip3 install flask 
sudo pip3 install flask-restful
