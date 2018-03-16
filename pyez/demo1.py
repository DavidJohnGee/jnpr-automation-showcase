from jnpr.junos import Device
from getpass import getpass
import sys

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)

try:
    dev.open()
except Exception as err:
    print (err)
    sys.exit(1)

print (dev.facts)
dev.close()
