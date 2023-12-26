#!/bin/bash -i

sudo -i

cd /home/ubuntu

nohup python3 gatekeeper.py PROXY_PRIVATE_DNS > log.txt 2>&1 &