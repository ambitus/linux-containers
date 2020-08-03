# Grafana
Grafana provides a framework for creating dashboards of time series data that users
access through a browser.  It is often used to monitor platform and application
resource usage metrics to help administrators operate their systems.  This example
demonstrates the common practice of aggregating several open source packages to
create a workload.

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
passes the aggregated information into _**grafana**_ for presentation.

## Building the Images

All of these Docker images have to be built on an IBM Z platform - either Linux on
Z running Docker, or an IBM zCX appliance.  Once all four of the images are built,
they can be run to create a functional monitoring environment that users consume
through Grafana.

Start by logging into the platform where you will build the images - either an IBM
zCX appliance, or a Linux on Z system with access to the internet.

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Total Build time | ~45 minutes |
| Prometheus image size | ~450 MB |
| node_exporter image size | ~135 MB |
| cAdvisor image size | ~550 MB |
| Grafana image size | ~1.25 GB |
| **Total footprint** | **~2.4 GB** |

**Build Prometheus**
Prometheus collects metrics based on end points defined in a configuration file
called ```prometheus.yml```. You can either build this configuration file into
the Docker image or point to it when launching Docker as a container.

1. Create a directory within your home directory, and cd into it. We recommend
naming it prometheus.
2. Download the Prometheus Dockerfile from
[https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Prometheus/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Prometheus/Dockerfile)
into ```$HOME/prometheus```
3. Build the Prometheus image:
- ```docker build -t prometheus .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged prometheus.1.7.1:latest```

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

**Build Grafana**
1. Create a directory within your home directory, and cd into it. We recommend
naming it ```grafana```.
2. Download the Grafana Docker file from
[https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Grafana/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/Grafana/Dockerfile)
into ```$HOME/grafana```
3. Build the Grafana image:
- ```docker build -t grafana .``` (be sure to include the .)

When the build is complete, you should see:
- ```Successfully tagged grafana.4.4.1:latest```

The version number may be different than ```latest```.

**Survey Your Images**

Now run ```docker images``` from the command line to verify the existence of all 4
images you have just built.  The sizes of these images should roughly match the
values in the image attributes table above.

## Run the Containers
Once the containers have been built, they are ready to run.  If you have created
these images on a Linux on Z system, you will have to transport the images to the
target zCX appliance through a save/ftp/load operation, or by push/pull to/from
a common image registry (e.g. Dockerhub).  If you build on the zCX appliance where
the containers will be running, everything is ready to go.

All of these containers will communicate with each other using a common Docker
network.  First, create this network, which we'll call ```monitoring```.

```
docker network create monitoring
```

**Start Prometheus**

```
docker run --name prometheus --network monitoring -p 9090:9090 -d prometheus
```

**Start cAdvisor**

```
docker run -v /proc:/rootfs/proc:ro -v /media:/rootfs/media:ro \
-v /var/run/docker.sock:/var/run/docker.sock:ro -v /sys:/sys:ro \
-v /var/lib/docker/:/var/lib/docker:ro -v /dev/disk/:/dev/disk:ro \
-p 8080:8080 -d --network monitoring --name=cadvisor cadvisor
```

**Start node_exporter**

```
docker run --name nodeexporter -v /proc:/host/proc -v /sys:/host/sys:ro \
-v /media:/rootfs/media:ro -v /etc/hostname:/etc/host_hostname:ro -p 9100:9100 -d \
--network monitoring nodeexporter
```

**Start Grafana**

```
docker run --name grafana --network monitoring -p 3000:3000 -d grafana
```

## Use the Grafana Web Interface
Once all of the containers are running, open a web browser, and navigate
to ```<appliance_ip>:3000```.  You will be presented with a login page, where you
need to set the password for a user the first time you log in.

At this point, you can use the interface as outlined at the Grafana project site
[https://grafana.com/](https://grafana.com/).
