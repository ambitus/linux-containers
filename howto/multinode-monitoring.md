# How to monitor multi zCX appliances using Grafana

One can monitor multi zCX appliances as follows (see the figure below):

1. Each zCX node to be monitored runs an instance of cAdvisor and Node Exporter
2. One of the zCX nodes runs Prometheus and Grafana together.  (Alternatively, Prometheus and Grafana can be run on separate nodes.)
3. Prometheus configuration file *prometheus.yml* should be modified to incorporate all the data collection end points for cAdvisor and Node Exporter

|![image for multi-node monitoring](https://github.com/gunaly/linux-containers/blob/master/howto/images/MultiNodeMonitoring.jpg )|
|:--:| 
|**Multinode monitoring: Direction on the arrows is the direction of polling/requests**|

## Prometheus configuration file for multi-node monitoring

The *scrape_configs* block in the *prometheus.yml* configuration file should be modified such that the end-points for all zCX nodes, both for nodeexporter and cadvisor, are added.  

For instance, cadvisor entry will read as follows:
```
 - job_name: 'cadvisor'
    scrape_interval: 1m
    scrape_timeout:  1m
    static_configs:
         - targets: ['IP1:Port1','IP2:Port2',…,'IPN:portN']
```

Here IP1 to IPN are the IP addresses (or hostnames) of the zCX nodes to be monitored and Port1 to PortN are the ports that cAdvisor instances listen to.  (They may all be the same default cAdvisor port.)

Similarly, Node Exporter polling can be configured as follows:
```
 - job_name: 'nodeexporter'
    scrape_interval: 1m
    scrape_timeout:  1m
    static_configs:
            - targets: [['IP1:Port1','IP2:Port2',…,'IPN:portN']]
```

Once these updates are introduced, Prometheus should be run with this configuration file.  

Assume you are started Prometheus as follows:
```
docker run --name prometheus -p 9090:9090 -d <prometheus_image_name>
```

Now, copy the new *prometheus.yml* file you edited for multi-node support to the running Prometheus container as follows:
```
docker cp prometheus.yml  prometheus:/etc/prometheus/
```

Finally, restart your Prometheus instance as follows:
```
docker restart Prometheus
```

## Grafana dashboard template for multi-node monitoring

A Grafana dashboard template to monitor multi zCX appliances can be downloaded from here https://grafana.com/grafana/dashboards/11855


