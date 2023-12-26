#!/bin/bash -i

sudo -i

cd /home/ubuntu

nohup python3 proxy.py MASTER_PRIVATE_DNS --slaves_dns SLAVE1_PRIVATE_DNS SLAVE2_PRIVATE_DNS SLAVE3_PRIVATE_DNS > log.txt 2>&1 &