# Apache Kafka
Apache Kafka is a distributed streaming platform that lets one endpoint in a workload
produce messages, while other endpoints consume them.  One or more consumers may subscribe
to messages under a topic that a producer publishes.  This architecture facilitates
communication between loosely coupled applications in an enterprise.

See [https://kafka.apache.org/](https://kafka.apache.org/) for more information

## Building and Running Apache Kafka
The Dockerfile for an Apache Kafka image can be found at the Linux-on-IBM-Z examples
github:

- [https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/ApacheKafka/Dockerfile](https://github.com/linux-on-ibm-z/dockerfile-examples/blob/master/ApacheKafka/Dockerfile)

Copy this Dockerfile a working location on your appliance (```~/apache_kafka``` in this
example).

- Build the image
  ```
	~/apache_kafka$ docker build --tag apache_kafka .
	```
- Run the container
  ```
	~/apache_kafka$ docker run --name apache_kafka -p 2081:2081 -p 9092:9092 -d apache_kafka
  749b65c869d4b91abde450f90961723e394a0e72bb16de3aae86ca6a40e90537
	```

This will start the Kafka server, which will listen for requests from producers and
consumers.  Note that the server takes several seconds to fully initialize.  If you try
to use it too quickly, you may temporarily see warnings like this:

```
Connection to node -1 (localhost/127.0.0.1:9092) could not be established. Broker may not be available.
```

**Important Image Attributes:**

| Attribute     | Value        |
|---------------|--------------|
| Total Build time | ~1 minute  |
| Image size | ~600 MB |
| **Total footprint** | **~600 MB** |

## A Simple Use Case
This use case illustrates a producer that creates a topic and generates a stream of
messages that are received by a consumer and displayed.  Both the producer and consumer
run in the same zCX appliance for this use case, but either could be located on any
platform.

In order to run this use case, please open 2 shell sessions via ssh into your appliance,
and sftp the test text file ('''sonnet-XVIII.txt''') to the same directory where you
have your Dockerfile

- _**Producer**_ - Create a topic

```
~/apache_kafka$ docker exec apache_kafka bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic simple-test-topic
```
- _**Producer**_ - List all topics

```
~/apache_kafka$ docker exec apache_kafka bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

- _**Producer**_ - Send some messages

```
~/apache_kafka$ docker exec -i apache_kafka bin/kafka-console-producer.sh < sonnet-XVIII.txt --bootstrap-server localhost:9092 --topic simple-test-topic
```

_**Consumer**_ - Read the producer's messages

```
~/apache_kafka$ docker exec apache_kafka bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic simple-test-topic --from-beginning
```

You should see this text arrive at the consumer:

```
Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade
Nor lose possession of that fair thou owest;
Nor shall Death brag thou wander'st in his shade,
When in eternal lines to time thou growest:
So long as men can breathe or eyes can see,
So long lives this and this gives life to thee.
```

_**CTRL_C**_ to exit the consumer.

You can also run this test with an interactive producer when executing the _Send
some messages_ step above like this:

```
~/apache_kafka$ docker exec -it apache_kafka bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic simple-test-topic
```

Once running, any text you enter at the prompt will be echoed to the consumer.  As
with the consumer, _**CTRL_C**_ to exit the producer.
