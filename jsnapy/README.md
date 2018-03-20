## JSNAP(y)

This is the Python version of a tool called JSNAP. This tool provides validation and testing mechanisms for Junos. It can take snapshots and compare then and also write out to a database.

## Installation from GitHub

```bash
sudo pip install git+https://github.com/Juniper/jsnapy.git 
```

Next, we use JSNAPy in the following way (assuming the `config_check.yml` and `test_no_diff.yml` files are present).

```bash
jsnapy --snap pre -f config_check.yml

# Make a change to lo0.0 here. Delete it, create it, something...

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




