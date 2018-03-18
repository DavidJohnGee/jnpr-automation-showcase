import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from myTables.ConfigTables import UserConfigTable

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

dev = Device(host=hostname, user=username, passwd=password)

try:
    with Device(host=hostname, user=username, passwd=password) as dev:   

        userconf = UserConfigTable(dev)
        userconf.user = 'pyez'
        userconf.user_class = 'read-only'
        userconf.password = '$ABC123'
        userconf.append()

        userconf.lock()
        userconf.load(merge=True)
        userconf.pdiff()

        userconf.commit()
        userconf.unlock()

except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)

