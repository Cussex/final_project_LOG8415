#!/bin/bash -i

sudo -i

apt-get update > /dev/null 2>&1

#Install Mysql cluster
mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home
wget -q http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
tar -xzf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz 1>/dev/null
ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc

echo 'export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc' > /etc/profile.d/mysqlc.sh
echo 'export PATH=$MYSQLC_HOME/bin:$PATH' >> /etc/profile.d/mysqlc.sh
source /etc/profile.d/mysqlc.sh

apt-get update && apt-get -y install libncurses5 > /dev/null 2>&1

#Master setup 
mkdir -p /opt/mysqlcluster/deploy
cd /opt/mysqlcluster/deploy
mkdir conf
mkdir mysqld_data
mkdir ndb_data
cd conf

#MySQL config
cat > my.cnf << EOF
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
port=3306
EOF

#MySQL cluster config
cat > config.ini << EOF
[ndb_mgmd]
hostname=MASTER_PRIVATE_DNS
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd default]
noofreplicas=3
datadir=/opt/mysqlcluster/deploy/ndb_data
serverport=2202

[ndbd]
hostname=SLAVE1_PRIVATE_DNS
nodeid=3

[ndbd]
hostname=SLAVE2_PRIVATE_DNS
nodeid=4

[ndbd]
hostname=SLAVE3_PRIVATE_DNS
nodeid=5

[mysqld]
nodeid=6
hostname=MASTER_PRIVATE_DNS

[mysqld]
nodeid=7
hostname=SLAVE1_PRIVATE_DNS

[mysqld]
nodeid=8
hostname=SLAVE2_PRIVATE_DNS

[mysqld]
nodeid=9
hostname=SLAVE3_PRIVATE_DNS
EOF

cd /opt/mysqlcluster/home/mysqlc
scripts/mysql_install_db --no-defaults --datadir=/opt/mysqlcluster/deploy/mysqld_data 1>/dev/null

#Start the management node
cd /opt/mysqlcluster/home/mysqlc/bin
ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf 1>/dev/null

#Install sysbench
apt-get install sysbench -y > /dev/null 2>&1