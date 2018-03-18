import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

dev = Device(host=hostname, user=username, passwd=password).open()
with Config(dev, mode='private') as cu:
    cu.load('set system services telnet', format='set')
    cu.pdiff()
    cu.commit()

sys.exit(0)
