from jnpr.junos import Device
from getpass import getpass
from lxml import etree
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

print "--- XML Output through issuing RPC call"
sw = dev.rpc.get_route_information()
print(etree.tostring(sw, encoding='unicode'))

print "--- JSON Output through issuing RPC call"
sw = dev.rpc.get_route_information({'format':'json'})
print(sw)

dev.close()

