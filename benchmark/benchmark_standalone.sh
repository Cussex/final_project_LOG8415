#!bin/bash -i

sudo -i

sysbench --table-size=1000000 --db-driver=mysql --mysql-user=root --mysql-db=sakila --time=60  --threads=6 --max-requests=0 /usr/share/sysbench/oltp_read_write.lua prepare 2>&1>/dev/null

sysbench --table-size=1000000 --db-driver=mysql --mysql-user=root --mysql-db=sakila --time=60  --threads=6 --max-requests=0 /usr/share/sysbench/oltp_read_write.lua run 2>&1>/home/ubuntu/benchmark.log

sysbench --db-driver=mysql --mysql-user=root --mysql-db=sakila /usr/share/sysbench/oltp_read_write.lua cleanup 2>&1>/dev/null
