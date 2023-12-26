#!/bin/bash -i

sudo -i

apt-get update > /dev/null 2>&1

#Install mysql standalone server
apt-get install mysql-server -y > /dev/null 2>&1

#Install sakila
mkdir /home/sakila
cd /home/sakila
wget -q https://downloads.mysql.com/docs/sakila-db.tar.gz 
tar -xzf sakila-db.tar.gz

#Sakila config
mysql -Bse "SOURCE /home/sakila/sakila-db/sakila-schema.sql;SOURCE /home/sakila/sakila-db/sakila-data.sql;" 1>/dev/null

#Install sysbench
apt-get install sysbench -y > /dev/null 2>&1