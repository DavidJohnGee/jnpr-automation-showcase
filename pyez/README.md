## PyEZ - Python SDK for Junos

This demo covers PyEZ; the Python SDK for Junos.

This is a programmatic abstraction layer over Junos. It uses NETCONF underneath to obtain and create objects in Python.

It is great for scripting, integration applications and troubleshooting.

__Install__

Information to install PyEZ can be located [here](https://www.juniper.net/documentation/en_US/junos-pyez/information-products/pathway-pages/junos-pyez-developer-guide.html).

```bash
sudo apt-get install python-pip python-dev libxml2-dev libxslt-dev libssl-dev libffi-dev
pip install junos-eznc

# if you want to install from source: pip install git+https://github.com/Juniper/py-junos-eznc.git
```

PyEZ is also available in a Docker image.

## Basic Usage

At it's most basic usage, we have to create a Device handler object, open a session (pass credentials), get information or make changes. Here is a script that allows us to connect and print 'device facts'.

```python
from jnpr.junos import Device
from getpass import getpass
import sys

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)

# Telnet connection
#dev = Device(host=hostname, user=username, passwd=password, mode='telnet', port='23')

# Serial console connection
#dev = Device(host=hostname, user=username, passwd=password, mode='serial', port='/dev/ttyUSB0')

try:
    dev.open()
except Exception as err:
    print (err)
    sys.exit(1)

print (dev.facts)
dev.close()
```

For ease, the Python file is in the directory where the README is being served from.

```bash
python demo1.py

Device hostname: "10.42.0.130"
Device username: "netconf"
Device password:
{'2RE': False, 'HOME': '/var/home/netconf', 'RE0': {'status': 'OK', 'last_reboot_reason': 'Router rebooted after a normal shutdown.', 'model': 'RE-VMX', 'up_time': '1 hour, 55 minutes, 57 seconds', 'mastership_state': 'master'}, 'RE1': None, 'RE_hw_mi': False, 'current_re': ['re0', 'master', 'node', 'fwdd', 'member', 'pfem'], 'domain': 'entry', 'fqdn': '.entry', 'hostname': '', 'hostname_info': {'re0': ''}, 'ifd_style': 'CLASSIC', 'junos_info': {'re0': {'text': '17.4R1.16', 'object': junos.version_info(major=(17, 4), type=R, minor=1, build=16)}}, 'master': 'RE0', 'model': 'VMX', 'model_info': {'re0': 'VMX'}, 'personality': 'MX', 're_info': {'default': {'default': {'status': 'OK', 'last_reboot_reason': 'Router rebooted after a normal shutdown.', 'model': 'RE-VMX', 'mastership_state': 'master'}, '0': {'status': 'OK', 'last_reboot_reason': 'Router rebooted after a normal shutdown.', 'model': 'RE-VMX', 'mastership_state': 'master'}}}, 're_master': {'default': '0'}, 'serialnumber': 'VM5AAC042657', 'srx_cluster': None, 'srx_cluster_id': None, 'srx_cluster_redundancy_group': None, 'switch_style': 'BRIDGE_DOMAIN', 'vc_capable': False, 'vc_fabric': None, 'vc_master': None, 'vc_mode': None, 'version': '17.4R1.16', 'version_RE0': '17.4R1.16', 'version_RE1': None, 'version_info': junos.version_info(major=(17, 4), type=R, minor=1, build=16), 'virtual': True}
```

We can also place configuration on to devices, execute RPC calls via Python and retrieve XML and JSON. Here's another script retrieving route information from Junos via XML and JSON.

```python
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
```

To run this script:

```bash
python demo2.py
```

Finally, we can place configuration in numerous different ways. Through `Config`, and `ConfigTables` we can generate configuration changes and submit them to Junos.

```python
TODO
```

