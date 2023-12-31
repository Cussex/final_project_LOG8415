#!/bin/bash -i

sudo -i

#Run the mysqld process
nohup mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf --user=root > /home/ubuntu/sql.log 2>&1 &

sleep 20

apt-get update > /dev/null 2>&1

#Install sakila
mkdir /home/sakila
cd /home/sakila
wget -q https://downloads.mysql.com/docs/sakila-db.tar.gz 
tar -xzf sakila-db.tar.gz

#Sakila config
mysql -Bse "SOURCE /home/sakila/sakila-db/sakila-schema.sql;SOURCE /home/sakila/sakila-db/sakila-data.sql;" 1>/dev/null

#Create user root
mysql -Bse "CREATE USER 'root'@'%';GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;FLUSH PRIVILEGES;" 1>/dev/null