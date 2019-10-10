# Grafana
Grafana is a graphical interface to Docker and platform resource usage.  Grafana
aggregates several metrics into provide an operational view of applications running
inside of an IBM zCX Docker appliance.

There are four Docker images that make up what we are calling the Grafana monitoring
interface:

- _**Grafana**_ - the graphical interface that provides a Dashboard view of resource
  use.
- _**Prometheus**_ - a metrics database used to assemble the data shown by Grafana.
- _**cAdvisor**_ - records metrics about running Docker containers.
- _**node_exporter**_ - records platform metrics.  Provides a view of resources
  used within an IBM zCX appliance.

_**cAdvisor**_ and _**node_exporter**_ collect and feed time-sequenced information
about running containers and appliance resource usage to _**prometheus**_, which then
passes the aggregated information into _**grafana**_ for presentation to users
through a web interface.

## Building the Images

All of these Docker images have to be built on an IBM Z platform - either Linux on
Z running Docker, or an IBM zCX appliance.  Once all four of the images are built,
can be run to create a functional monitoring environment that can be accessed by
a user through the Grafana interface.

Start by logging into the platform where you will build the images - either an IBM
zCX appliance, or a Linux on Z system with access to the internet.

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Total Build time | 30 minutes |
| cAdvisor image size | ~xx MB |
| node_exporter image size | ~xx MB |
| Prometheus image size | ~xx MB |
| Grafana image size | ~xx MB |

**Build Prometheus**
Prometheus collects metrics based on end points defined in a configuration file
called ```prometheus.yml```. You can either build this configuration file into
the Docker image or point to it when launching Docker as a container.

1. Create a directory within your home directory, and cd into it. We recommend
naming it prometheus.
2. Download the Prometheus Dockerfile from
[https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Prometheus/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Prometheus/Dockerfile)
3. Build the Prometheus image:
- ```docker build -t prometheus .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged prometheus.1.7.1:latest```

The version number may be different than ```latest```.

**Build node_exporter:**
1. Create a directory within your home directory, and cd into it. We recommend naming
   it nodeexporter.
2. Save the text below into a file named Dockerfile:
```
########## Dockerfile for Node Exporter #########
#
#
# To build this image, from the directory containing this Dockerfile
# (assuming that the file is named Dockerfile):
# docker build -t <image_name> .
#########################################################################################################
# Base Image
FROM s390x/ubuntu:18.04
RUN apt-get update && apt-get install -y prometheus-node-exporter
EXPOSE 9100
CMD prometheus-node-exporter --path.procfs="/host/proc" --path.sysfs="/host/sys" --collector.diskstats --collector.loadavg --collector.meminfo --collector.netdev --collector.netstat --collector.stat --collector.time --collector.uname --collector.vmstat --collector.filesystem.ignored-mount-points="^/(sys|proc|dev|host|etc)($$|/)"
```
3. Build the node_exporter image:
- ```docker build -t nodexporter .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged nodeexporter:latest```

The version number may be different than ```latest```.

**Build cAdvisor:**
1. Create a directory within your home directory, and cd into it. We recommend naming
   it cadvisor.
2. Download the cAdvisor Dockerfile from
[https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/cAdvisor/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/cAdvisor/Dockerfile)
into ```$HOME/cadvisor```.
3. Build the cAdvisor image:
- ```docker build -t cadvisor .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged cadvisor:latest```

The version number may be different than ```latest```.

**Build Grafana**
1. Create a directory within your home directory, and cd into it. We recommend
naming it ```grafana```.
2. Download the Grafana Docker file from
[https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Grafana/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Grafana/Dockerfile)
3. Build the Grafana image:
- ```docker build -t grafana .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged grafana.4.4.1:latest```

The version number may be different than ```latest```.

## Run the Containers

- ```coming soon```

## Use the Grafana Web Interface

- ```coming soon```
