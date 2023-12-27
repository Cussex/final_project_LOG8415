import subprocess
import boto3
import os
import time
from dotenv import load_dotenv
from functions import *

load_dotenv("credentials.env")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
#aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'LOG8415E'
securityGroupName = 'LOG8415E_B2'

# Create an EC2 client
EC2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    #aws_session_token=aws_session_token
)

WAITER = EC2.get_waiter('instance_status_ok')

# get vpc_id
vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
subnet = EC2.describe_subnets().get('Subnets', [{}])[0].get('SubnetId', '')

# create key pair and security group
print('Creating key pair...')
create_key_pair(EC2, keyPairName)
print('Creating security group...')
security_group = create_security_group(EC2, securityGroupName, vpc_id)

# launch instances
print('Launching standalone instance...')
standalone_id =  create_t2micro_instance(EC2, keyPairName, security_group['GroupId'], subnet, 'standalone')
print('Launching master instance...')
master_id =  create_t2micro_instance(EC2, keyPairName, security_group['GroupId'], subnet, 'master')
print('Launching 3 slave instances...')
slave1_id =  create_t2micro_instance(EC2, keyPairName, security_group['GroupId'], subnet, 'slave1')
slave2_id =  create_t2micro_instance(EC2, keyPairName, security_group['GroupId'], subnet, 'slave2')
slave3_id =  create_t2micro_instance(EC2, keyPairName, security_group['GroupId'], subnet, 'slave3')

print('Launching proxy instance...')
proxy_id =  create_t2large_instance(EC2, keyPairName, security_group['GroupId'], subnet, "setup/proxy_setup.sh", 'proxy')
print('Launching gatekeeper instance...')
gatekeeper_id =  create_t2large_instance(EC2, keyPairName, security_group['GroupId'], subnet, "setup/gatekeeper_setup.sh", 'gatekeeper')

WAITER = EC2.get_waiter('instance_status_ok')
WAITER.wait(InstanceIds=[standalone_id, master_id, slave1_id, slave2_id, slave3_id, proxy_id, gatekeeper_id])

print("All instances are running")

#Private dns
master_private_dns = EC2.describe_instances(InstanceIds=[master_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']
slave1_private_dns = EC2.describe_instances(InstanceIds=[slave1_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']
slave2_private_dns = EC2.describe_instances(InstanceIds=[slave2_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']
slave3_private_dns = EC2.describe_instances(InstanceIds=[slave3_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']

proxy_private_dns = EC2.describe_instances(InstanceIds=[proxy_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']
gatekeeper_private_dns = EC2.describe_instances(InstanceIds=[gatekeeper_id])['Reservations'][0]['Instances'][0]['PrivateDnsName']

#Public dns
standalone_dns = EC2.describe_instances(InstanceIds=[standalone_id])['Reservations'][0]['Instances'][0]['PublicDnsName']
master_dns = EC2.describe_instances(InstanceIds=[master_id])['Reservations'][0]['Instances'][0]['PublicDnsName']
slave1_dns = EC2.describe_instances(InstanceIds=[slave1_id])['Reservations'][0]['Instances'][0]['PublicDnsName']
slave2_dns = EC2.describe_instances(InstanceIds=[slave2_id])['Reservations'][0]['Instances'][0]['PublicDnsName']
slave3_dns = EC2.describe_instances(InstanceIds=[slave3_id])['Reservations'][0]['Instances'][0]['PublicDnsName']

proxy_dns = EC2.describe_instances(InstanceIds=[proxy_id])['Reservations'][0]['Instances'][0]['PublicDnsName']
gatekeeper_dns = EC2.describe_instances(InstanceIds=[gatekeeper_id])['Reservations'][0]['Instances'][0]['PublicDnsName']

# Replace private dns in setup files
subprocess.call(["sed", "-i", "", "s/MASTER_PRIVATE_DNS/" + master_private_dns + "/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE1_PRIVATE_DNS/" + slave1_private_dns + "/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE2_PRIVATE_DNS/" + slave2_private_dns + "/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE3_PRIVATE_DNS/" + slave3_private_dns + "/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/MASTER_PRIVATE_DNS/" + master_private_dns + "/g", "setup/slave_setup.sh"])

subprocess.call(["sed", "-i", "", "s/PROXY_PRIVATE_DNS/" + proxy_private_dns + "/g", "gatekeeper/deploy_gatekeeper.sh"])
subprocess.call(["sed", "-i", "", "s/MASTER_PRIVATE_DNS/" + master_private_dns + "/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE1_PRIVATE_DNS/" + slave1_private_dns + "/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE2_PRIVATE_DNS/" + slave2_private_dns + "/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/SLAVE3_PRIVATE_DNS/" + slave3_private_dns + "/g", "proxy/deploy_proxy.sh"])

print("Configuring instances...")
os.system("chmod 700 " + keyPairName + ".pem")

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + standalone_dns + " 'bash -s' < setup/standalone_setup.sh 1>/dev/null")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + master_dns + " 'bash -s' < setup/master_setup.sh 1>/dev/null")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave1_dns + " 'bash -s' < setup/slave_setup.sh 1>/dev/null")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave2_dns + " 'bash -s' < setup/slave_setup.sh 1>/dev/null")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave3_dns + " 'bash -s' < setup/slave_setup.sh 1>/dev/null")

subprocess.call(["sed", "-i", "", "s/" + master_private_dns + "/MASTER_PRIVATE_DNS/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave1_private_dns + "/SLAVE1_PRIVATE_DNS/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave2_private_dns + "/SLAVE2_PRIVATE_DNS/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave3_private_dns + "/SLAVE3_PRIVATE_DNS/g", "setup/master_setup.sh"])
subprocess.call(["sed", "-i", "", "s/" + master_private_dns + "/MASTER_PRIVATE_DNS/g", "setup/slave_setup.sh"])

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + master_dns + " 'bash -s' < setup/master_setup_2.sh")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave1_dns + " 'bash -s' < setup/slave_setup_2.sh")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave2_dns + " 'bash -s' < setup/slave_setup_2.sh")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + slave3_dns + " 'bash -s' < setup/slave_setup_2.sh")

print("All instances are configured")

print("Running benchmark on standalone instance...")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + standalone_dns + " 'bash -s' < benchmark/benchmark_standalone.sh")
os.system("scp -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + standalone_dns + ":~/benchmark.log ./benchmark/results/standalone.txt")
print("Results saved in benchmark/results/standalone.txt")

print("Running benchmark on cluster...")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + master_dns + " 'bash -s' < benchmark/benchmark_cluster.sh")
os.system("scp -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + master_dns + ":~/benchmark.log ./benchmark/results/cluster.txt")
print("Results saved in benchmark/results/cluster.txt")

print("Deploying proxy...")
os.system("scp -o StrictHostKeyChecking=no -i " + keyPairName + ".pem -r proxy/proxy.py ubuntu@" + proxy_dns + ":~/")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + proxy_dns + " 'bash -s' < proxy/deploy_proxy.sh")
subprocess.call(["sed", "-i", "", "s/" + master_private_dns + "/MASTER_PRIVATE_DNS/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave1_private_dns + "/SLAVE1_PRIVATE_DNS/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave2_private_dns + "/SLAVE2_PRIVATE_DNS/g", "proxy/deploy_proxy.sh"])
subprocess.call(["sed", "-i", "", "s/" + slave3_private_dns + "/SLAVE3_PRIVATE_DNS/g", "proxy/deploy_proxy.sh"])
print("Proxy deployed")

print("Deploying gatekeeper...")
os.system("scp -o StrictHostKeyChecking=no -i " + keyPairName + ".pem -r gatekeeper/gatekeeper.py ubuntu@" + gatekeeper_dns + ":~/")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + gatekeeper_dns + " 'bash -s' < gatekeeper/deploy_gatekeeper.sh")
subprocess.call(["sed", "-i", "", "s/" + proxy_private_dns + "/PROXY_PRIVATE_DNS/g", "gatekeeper/deploy_gatekeeper.sh"])
print("Gatekeeper deployed")

time.sleep(20)

print("Testing proxy and gatekeeper...")

os.system("python3 client/client.py " + gatekeeper_dns + " > client/results.txt")

print("Done !")

input("Press Enter to delete everything...")

terminate_instance(EC2, standalone_id)
terminate_instance(EC2, master_id)
terminate_instance(EC2, slave1_id)
terminate_instance(EC2, slave2_id)
terminate_instance(EC2, slave3_id)
terminate_instance(EC2, proxy_id)
terminate_instance(EC2, gatekeeper_id)
WAITER = EC2.get_waiter('instance_terminated')
WAITER.wait(InstanceIds=[standalone_id, master_id, slave1_id, slave2_id, slave3_id, proxy_id, gatekeeper_id])
print("Instances terminated")

print("Deleting security group...")
delete_security_group(EC2, securityGroupName)

print("Deleting key pair...")
delete_key_pair(EC2, keyPairName)

