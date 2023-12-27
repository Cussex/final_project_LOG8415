#!/bin/bash -i
sudo -i

apt-get update > /dev/null 2>&1

#Mysql cluster config
mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home
wget -q http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
tar -xzf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz 1>/dev/null
ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc

echo 'export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc' > /etc/profile.d/mysqlc.sh
echo 'export PATH=$MYSQLC_HOME/bin:$PATH' >> /etc/profile.d/mysqlc.sh
source /etc/profile.d/mysqlc.sh

#Install libncurses5
apt-get update && apt-get -y install libncurses5 > /dev/null 2>&1

#Start data node
mkdir -p /opt/mysqlcluster/deploy/ndb_data
ndbd -c MASTER_PRIVATE_DNS:1186 1>/dev/null

#Setup sql node
mkdir -p /opt/mysqlcluster/deploy/conf
mkdir -p /opt/mysqlcluster/deploy/mysqld_data

cat > /opt/mysqlcluster/deploy/conf/my.cnf<< EOF
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
port=3306
ndb-connectstring=MASTER_PRIVATE_DNS:1186

[mysql_cluster]
ndb-connectstring=MASTER_PRIVATE_DNS:1186
EOF

cd /opt/mysqlcluster/home/mysqlc
scripts/mysql_install_db --no-defaults --datadir=/opt/mysqlcluster/deploy/mysqld_data 1>/dev/null

#Install sysbench
apt-get install sysbench -y > /dev/null 2>&1