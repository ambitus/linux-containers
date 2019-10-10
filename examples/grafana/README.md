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

## Use the Grafana Web Interface



------

## Promethius
Prometheus is an open-source toolkit for system monitoring and alerting. It was originally built by Soundcloud but is now a standalone and open-source project and maintained independently of any company.
5. Run the following command:
   - `docker images`
to see the Docker image prometheus in the list of images.
Use the following commands to run a Prometheus image:
   - `docker network create monitoring`
   - `docker run --name prometheus --network monitoring -p 9090:9090 -d prometheus`

The "monitoring" network is required only if Prometheus collects metrics locally.
In order for a Prometheus instance to collect metrics from a Prometheus-instrumented data collection agent, it must be configured with the agent's data collection end point, IP/Host name and port. Here is the content of a sample Prometheus configuration file that collects cAdvisor and Node Exporter metrics locally every 15 seconds:

```# my global config
global:
scrape_interval: 15s # By default, scrape targets every 15 seconds.
evaluation_interval: 15s # By default, scrape targets every 15 seconds.
external_labels:
monitor: 'my-project'
# A scrape configuration containing exactly one endpoint to scrape:
scrape_configs:
- job_name: 'cadvisor'
scrape_interval: 1m
scrape_timeout: 1m
static_configs:
- targets: ['cadvisor:8080']
- job_name: 'nodeexporter'
scrape_interval: 1m
scrape_timeout: 1m
static_configs:
- targets: ['nodeexporter:9100']
```

Assuming that this configuration file named "prometheus.yml" and it resides in the Docker build directory, one can build this configuration file into a Prometheus Docker image by including the following line in the Dockerfile
   - COPY prometheus.yml /etc/prometheus/prometheus.yml

just before the CMD line in Prometheus Dockerfile.
Alternatively, the configuration file can be mounted at run-time to override the contents of the default /etc/prometheus/prometheus.yml configuration file. This approach is more preferable when the number of zCX appliances to monitor is expected to grow over time.
Refer to the Prometheus documentation for more detailed instructions on building a Prometheus configuration file: https://prometheus.io/docs/prometheus/latest/configuration/configuration/

## cAdvisor
cAdvisor collects, aggregates, processes, and exports metrics on running containers. The metrics are related to resource usage and performance characteristics.
Use the following steps to build a cAdvisor Docker image:


5. Run the following command:
   - `docker images`
to see the Docker image cadvisor in the list of images.
Use the following commands to deploy and run c Advisor. Skip the first command if the "monitoring" network has been created before:
   - `docker network create monitoring`
   - `docker run -v /:/rootfs:ro -v /var/run:/var/run:ro -v /sys:/sys:ro -v /var/lib/docker/:/var/lib/docker:ro -v /dev/disk/:/dev/disk:ro -p 8080:8080 -d –network monitoring --name=cadvisor`
   - `cadvisor`


## Grafana
Grafana allows you to query, visualize, set alerts for, and understand your system metrics regardless of where they are stored. You can also create, explore, and share dashboards with your team. In this set-up, the metrics will be maintained by Prometheus. A sample Grafana dashboard will be made available by IBM.

5. Run the following command:
   - `docker images`
to see the Docker image grafanain the list of images.
Use the following steps to run a Grafana image:
1. Run the following commands. Skip the first command if the "monitoring" network has been created before:
   - `docker network create monitoring`
   - `docker run --name grafana --network monitoring -p 3000:3000 -d grafana`
2. Browse to {host ip}:3000, which should give a Granada login screen
3. Change the default admin password and add users as needed.
4. Define a data source for your Prometheus instance and import the IBM zCX Grafana dashboard template or build your own dashboard from scratch
5. Click on the button labeled Home and select zCX for z/OS monitoring dashboard if you have the zCX Grafana dashboard imported.

## Node Exporter
Node Exporter collects a wide variety of Linux hardware and kernel related metrics.
Use the following steps to build a Node Exporter Docker image:

5. Run the following command:
   - `docker images`
to see the Docker image nodeexporter in the list of images.
Use the following commands to deploy and run Node Exporter. Skip the first command if the "monitoring" network has been created before:
   - `docker network create monitoring`
   - `docker run --name nodeexporter -v /proc:/host/proc:ro -v /sys:/host/sys:ro -v /:/rootfs:ro -v /etc/hostname:/etc/host_hostname:ro -p 9100:9100 -d --network monitoring nodeexporter`
