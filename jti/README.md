## JTI (Juniper Telemetry Interface)

This demo mainly focusses on the OpenConfig aspect of JTI and uses the JTIMon tool to demonstrate some simple capablities. Data delivered is via "universal key/value" pairs coded using GPB.

When it comes to the 'junos specific' type of streaming telemetry, that is configured from Junos and streamed to a collector.

## Build Instructions for OpenConfig JTI

1.	Install the [Junos OpenConfig](https://www.juniper.net/support/downloads/?p=openconfig#sw) package on the vMX
2.	Install the [Network Agent](https://www.juniper.net/support/downloads/?p=mx960#sw) package on the vMX

These agents have to be compatible and should not be randomly installed.

Grab the `JTIMon Go Client` to demonstrate the JTI with OpenConfig.

```bash
go get github.com/golang/protobuf/proto
go get github.com/gorilla/mux
go get github.com/influxdata/influxdb/client/v2
go get github.com/prometheus/client_golang/prometheus/promhttp
go get github.com/spf13/pflag
go get golang.org/x/net/context
go get google.golang.org/grpc
go get github.com/nileshsimaria/jtimon/telemetry
go get github.com/nileshsimaria/jtimon/authentication

git clone https://github.com/nileshsimaria/jtimon.git
cd jtimon
go build
```

Once built, try the app with the usual `-h` flag to make sure it's compiled and built.

```bash
$ ./jtimon -h
Usage of ./jtimon:
      --compression string   Enable HTTP/2 compression (gzip, deflate)
      --config string        Config file name
      --csv-stats            Capture size of each telemetry packet
      --drop-check           Check for packet drops
      --gtrace               Collect GRPC traces
      --latency-check        Check for latency
      --log string           Log file name
      --max-kv uint          Max kv
      --max-run int          Max run time in seconds
      --prefix-check         Report missing __prefix__ in telemetry packet
      --print                Print Telemetry data
      --prometheus           Stats for prometheus monitoring system
      --sleep int            Sleep after each read (ms)
      --stats int            Print collected stats periodically
      --time-diff            Time Diff for sensor analysis using InfluxDB
pflag: help requested
```

Load up the agent packages:

```bash
# Host
$ scp ~/Downloads/junos-openconfig-x86-32-0.0.0.9.tgz root@10.42.0.130:/var/tmp/junos-openconfig-x86-32-0.0.0.9.tgz
$ scp ~/Downloads/network-agent-x86-32-17.4R1.16-C1.tgz root@10.42.0.130:/var/tmp/network-agent-x86-32-17.4R1.16-C1.tgz

# Junos
request system software add /var/tmp/junos-openconfig-x86-32-0.0.0.9.tgz no-validate
request system software add /var/tmp/network-agent-x86-32-17.4R1.16-C1.tgz no-validate
```

Ensure this configuration is in place on Junos:

```bash
set system services extension-service request-response grpc clear-text port 50051
set system services extension-service request-response grpc skip-authentication
set system services extension-service notification port 1883
set system services extension-service notification allow-clients address 0.0.0.0/0
```

Next, let's create a configuration file for `JTIMon`.

```bash
cat jtimonconfig.json
{
    "host": "10.42.0.130",
    "port": 50051,
    "user": "netconf",
    "password": "Passw0rd",
    "cid": "jtimon1",
    "grpc" : {
        "ws" : 524288
    },
    "paths": [{
        "path": "/interfaces",
        "freq": 2000
    }, {
        "path": "/junos/system/linecard/cpu/memory/",
        "freq": 1000
    }, {
        "path": "/bgp",
        "freq": 10000
    }, {
        "path": "/components",
        "freq": 10000
    }]
}
```

Lastly, let's actually run the JTIMon tool and see some telemetry data flowing out of Junos via gRPC.

```bash
./jtimon/jtimon --config jtimonconfig.json --stats 10 --drop-check --print
```

Note, it's possible to use JTIMon to feed directly in to InfluxDB, to a log file and also integrate with Prometheus.

## OpenNTI

It's also possible to use another Juniper project called [OpenNTI](https://github.com/Juniper/open-nti) which builds dashboards for visualising the exported data. It uses InfluxDB, Fluentd and Grafana to build a performance monitor. OpenNTI can poll for NETCONF data and can also receive streaming telemtry from the native sensors on Junos.

OpenNTI includes a JTI collector for GPB based telemetry based on the MX and also an Analyticsd collector for the QFX range. GPB proto files are included in the OpenNTI collector allowing data to be decoded and inserted into InfluxDB.

It's possible to see what sensors are configured in Junos for us to take telemetry from with the JTI.

```bash
# Junos
show agent sensors
```

The next step is to install OpenNTI using the installation guide [here](http://open-nti.readthedocs.io/en/latest/install.html).
Once OpenNTI is installed, there are several steps of configuration on Junos that require committing along with some OpenNTI specific configuration.

```bash
set services analytics streaming-server "demo vm" remote-address 10.42.0.128
set services analytics streaming-server "demo vm" remote-port 50000

set services analytics export-profile "Demo profile" local-address 10.42.0.130
set services analytics export-profile "Demo profile" local-port 50500
set services analytics export-profile "Demo profile" reporting-rate 30
set services analytics export-profile "Demo profile" format gpb
set services analytics export-profile "Demo profile" transport udp

set services analytics sensor "Demo sensor" server-name "demo vm"
set services analytics sensor "Demo sensor" export-name "Demo profile"
set services analytics sensor "Demo sensor" resource /junos/system/linecard/interface/
```

The configuration is fairly straight forward. First, configure a streaming server. Next, configure an export-profile. Finally, configure a sensor. One sensor is related to one resource. If you want more than one exported data set, then configure multiple sensors.

In order to configure the rest of OpenNTI, follow the instruction guides. It is possible for OpenNTI to query a Junos device for XML information, allowing different dashboards to be created from different sourced metrics.

It's also possible to use the IDL files (.proto) to decode captured information. If you want to take a peak at what the data looks like pre-decoding and post, follow [this](https://www.juniper.net/documentation/en_US/junos/topics/reference/general/junos-telemetry-interface-decoding-data.html) guide.

## Close

The most import thing to remember with the JTI is there are two different data models for two different things.
a) The OpenConfig YANG models allow for GPB encoded key/value pairs to be created for some metrics. These metrics will be transmitted in the same TCP session used to subscribe to the metrics of interest.
b) The Junos specific models and associated `.proto` files are for sensor streaming and are transmitted in UDP.
