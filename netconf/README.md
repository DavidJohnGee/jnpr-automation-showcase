## README for NETCONF Demo

This demonstrates how to use NETCONF on a Junos.

__Basic NETCONF__

NETCONF is a protocol based on RFC6241 that provides an XML interface for configuration data as well as protocol messages. NETCONF runs over TCP and is a critical foundational block of Junos.

It allows you to push configuration against the running or a candidate configuration and retrieve operational information. NETCONF calls for Junos are modelled in YANG. You never actually see YANG, but rather the XML data structrures derived from YANG data models.

I've created a user called "netconf" with the login class "superuser" with plaintext authentication.

```bash
set system login user netconf class super-user
set system login user netconf authentication encrypted-password "$6$SrgJyWtT$7Xfo8RLM7ncq4Q6MeNTBL1Bk7WurwgiFne1WUJL63ke3FTk9oUDqIIn0JEG3ClXsQtmLBIzlBWBJVt.h09fnk1"
commit
```

Now we can open an SSH session up and say hello with NETCONF.

```bash
ssh netconf@10.42.0.130 netconf

# Paste in the below
  <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
    <capability>http://xml.juniper.net/netconf/junos/1.0</capability>
  </capabilities>
</hello>
]]>]]>
```

Next, let's take a show command and demonstrate how to turn this in to a NETCONF call.

```bash
show system information | display xml rpc

  <rpc>
      <get-system-information>
      </get-system-information>
  </rpc>
]]>]]>
```

Even the CLI is wired in to the XML subsystem as you can clearly see.

Next, let's take some simple code and show how easy it becomes to script with NETCONF and build code!

```bash
go get github.com/Juniper/go-netconf/netconf

cd /home/davidgee/go/src/github.com/Juniper/go-netconf/examples/juniper

# Junos: set system services netconf ssh port 830
#        commit

make all

./get_system_information -host 10.42.0.130
Enter a valid username: netconf
Enter Password:
hostname:
model: vmx
version: 17.4R1.16
```

In Python there is a popular library called 'ncclient'.
