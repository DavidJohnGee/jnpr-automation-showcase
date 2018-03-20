## JTI (Juniper Telemetry Interface)

1.	Install the [Junos OpenConfig](https://www.juniper.net/support/downloads/?p=openconfig#sw) package on the vMX
2.	Install the [Network Agent](https://www.juniper.net/support/downloads/?p=mx960#sw) package on the vMX

These agents have to be compatible and should not be randomly installed.

Grab the `JTIMon Go Client` to demonstrate the JTI.

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

Ensure this configuration is in place on Junos:

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

It's possible to see what sensors are configured in Junos for us to take telemetry from with the JTI.

```bash
# Junos
show agent sensors
```

Lastly, let's actually run the JTIMon tool and see some telemetry data flowing out of Junos via gRPC.

```bash
./jtimon/jtimon --config jtimonconfig.json --stats 10 --drop-check --print
```

## OpenNTI

It's also possible to use another Juniper project called [OpenNTI](https://github.com/Juniper/open-nti) which builds dashboards for visualising the exported data.

OpenNTI is however out of scope currently for this demo showcase and if one is shown, it's at the demonstrators own desire.
