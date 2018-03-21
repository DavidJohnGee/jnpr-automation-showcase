## JSNAP(y)

This is the Python version of a tool called JSNAP. This tool provides validation and testing mechanisms for Junos. It can take snapshots and compare then and also write out to a database.

## Installation from GitHub

```bash
sudo pip install git+https://github.com/Juniper/jsnapy.git 
```

The JNSAP(y) config looks like below:

```bash
# Example from JNSAPy guide.
hosts:
  - device: vMX01
    username : netconf
    passwd: Passw0rd
tests:
  - test_no_diff.yml
```

The actual test looks like this:

```bash
# test_no_diff.yml
test_interface_status:
  - command: show interfaces terse lo*
  - iterate:
      xpath: physical-interface/logical-interface
      id: './name'
      tests:
        - no-diff: admin-status
          err: "Test Failed!! admin-status  got changed, before it was <{{pre['admin-status']}}>, now it is <{{post['admin-status']}}>"
          info: "Test Passed!! admin-status is same, before it is <{{pre['admin-status']}}> now it is <{{post['admin-status']}}>"
```

Next, we use JSNAPy in the following way (assuming the `config_check.yml` and `test_no_diff.yml` files are present).

```bash
jsnapy --snap pre -f config_check.yml

# Make a change to lo0.42. Disable it!
# set interfaces lo0.42 disable

jsnapy --snap post -f config_check.yml
jsnapy --check pre post -f config_check.yml
jsnapy --diff pre post -f config_check.yml
```

Be sure to clear out the snapshots when finished!

```bash
rm ~/jsnapy/snapshots/*
```

## Close

More information is available [https://github.com/Juniper/jsnapy](https://github.com/Juniper/jsnapy).




