 Copyright Contributors to the Ambitus Project.

SPDX-License-Identifier: Apache-2.0

# ELK Stack on zCX

This set of instructions shows how to run the ELK stack, consisting of Elasticsearch, Logstash and Kibana, together as containers on a zCX appliance. We will use the containers to recieve, process, and display a stream of data from outside of the appliance. In this case, Twitter activity. 

## Building the Containers

The docker images used for this demonstration come from the linux-on-ibm-z/dockerfile-examples repository.
https://github.com/linux-on-ibm-z/dockerfile-examples

Be sure to avoid the version of Elasticsearch from our registry, as it is incompatible with this repositories' versions of Logstash and Kibana. Instead, use this repositories' version of Elasticsearch, Logstash, and Kibana.

After connecting to your zCX Appliance, clone this repository and build Elasticsearch, Logstash, and Kibana via 

`docker build -t elasticsearch dockerfile-examples/Elasticsearch/`

`docker build -t logstash dockerfile-examples/Logstash/`

`docker build -t kibana dockerfile-examples/Kibana/`

To build each of the three containers from their respective dockerfiles. 

## Running the Containers

First we'll create a Docker network to use for our demo:

`docker network create elk`

Next, we'll run our Elasticsearch container. This can be run very simply with

`docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name elasticsearch --network elk -d elasticsearch`

Now, we must run our Logstash container. This will require a bit more setup before we run it, via configuration files.

Use a text editor to create a file `logstash_twitter.conf` containing the following content:

```
# logstash_twitter.conf
input {
  twitter {
    consumer_key => "KEY"
    consumer_secret => "SECRET"
    oauth_token => "TOKEN"
    oauth_token_secret => "TOKEN SECRET"
    keywords => [ "IBM", "Redhat", "Watson" ]
    full_tweet => true
  }
}

output {
 stdout { codec => dots }
 elasticsearch {
 action => "index"
 index => "twitter"
 hosts => "elasticsearch"
 document_type => "tweet"
 template => "/app/twitter_template.json"
 template_name => "twitter"
 workers => 1
 }
}
```

You see that this configuration requires API keys - navigate to `developer.twitter.com` and register an account, then create a New Application from their web interface.
Name it whatever you like. Under the new applications' "Keys and tokens" tab, you can generate a Consumer API Key / Secret pair, and an Authentication Bearer Token and Access token/Secret.
These should be filled in for the values of `consumer_key`, `consumer_secret`, `oauth_token`, and `oauth_token_secret` in the conf file.
You'll see that the configuration file also requires a template for the Twitter data, via the file `.twitter_template.json`. This can be pulled from
https://github.com/elastic/examples/blob/master/Common%20Data%20Formats/twitter/twitter_template.json
Where it is provided under the Apache 2.0 License. 

Add both `logstash_twitter.conf` and `twitter_template.json` to a new Docker volume `elkvol`, and you're ready to run Logstash! Run the container and enter the shell with

`docker run -it --rm --name logstash --link elasticsearch --network elk --mount source=elkvol,target=/app --entrypoint bash logstash`

And then begin collecting data by running 

`logstash -f /app/logstash_twitter.conf`

Logstash is now running and actively collecting data! Back outside the container shell, we still need to run Kibana. Kibana also requires a configuration file, which we'll pull back from the linux-on-ibm-z/dockerfile-examples repo,
where a configuration file can be found under `ELK/config/kibana.yaml`. We need to update this file by adding the following lines at the bottom of the file:
```
elasticsearch.hosts: ["http://URL:9200"]
#server.host: "URL"
server.host: "127.0.0.1"
```

In which `URL` should be replaced by the URL of your zCX container, and add it to the same volume elkvol. 

Now we can run Kibana via 

`docker run --name kibana -p5601:5601 --link elasticsearch --mount source=elkvol,target=/usr/share/kibana/config/ --network elk kibana`

## Kibana Visualization

We can access our Kibana container via a web browser at `URL:5061`, from which `URL` is the URL of the zCX container. 

On the kibana Web Page, we can click the "Discover" button to the left of the screen and create a New Index. This index should have
Index Pattern: `Twitter`
and
timestamp: `\@timestamp` with the `simple` option selected. This references the data that's being added to the Elasticsearch container's `twitter` index 
by our Logstash container.

At this point, Kibana is running! Try a query like `text:IBM OR text:Redhat OR text:Watson` under a Pie Chart via the "visualize" tab. Use 
Buckets->Split Slices with the bucket aggregates
`text:IBM`
`text:Redhat`
`text:Watson`
To compare the number of tweets referencing each over a selected timeframe.

![IMS](/ELK_stack_demo_twitter/pieChartKibana.PNG?raw=true)
