# Grafana Demo FOREX
A demonstration in Elasticsearch and Grafana run on a zCX appliance to display external data

This README shows how to set up and run Elasticsearch and Grafana in Docker containers on a zCX appliance, 
using them along with a background python script to pull, store, and display live Foreign Exchange data from
outside of the appliance.

# Running the Containers

First, SSH into a running zCX appliance. The following commands should be run:

`docker network create monitoring` creates a new docker Network. We call the network "monitoring", since we'll be
monitoring diagnostic infomation in this demo. All containers will be run on this network.

`docker run --name grafana --network monitoring -p 3000:3000 -d 9.12.21.147:5000/grafana` will pull and run a working Grafana image
from our registry. Flags are used to specify the container's name, network, and port. 

`docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name elasticsearch --network monitoring -d 9.12.21.147:5000/elastic
` will pull and run a working Elasticsearch image from our registry. Once again, flags are used to specify the container's name, network, and port. 

# Setting up our Data Source

For this demonstration, we are going to display a live feed for Foreign Exchange price information, provided by the Alphavantage API.
We'll use a Python script to query the API and insert the obtained info into our Elasticsearch container. `backgroundForex.py`, in this
repository, is that script. Here we explain it's function line by line:

First, we need an API key, which can be obtained for free at https://www.alphavantage.co/support/#api-key , and you may need to work inside an Ubuntu container or similar in order to have access to `apt-get`/`pip` to install the Python library dependencies. If you do this, make sure to run it on the `monitoring` network as well. 

`apt-get install pip`
`pip install requests`
`pip install json`
`pip install elasticsearch`

Before we run our script, let's look at the API call we're using: `CURRENCY_EXCHANGE_RATE` from Alphavantage. We'll pass in the parameters
`from_currency=USD`, `to_currency=EUR`, and our `apikey=### YOUR API KEY HERE ###` for the API key we obtained. The API call's URL looks like

`https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey=`

And returns 

`{"Realtime Currency Exchange Rate": {"1. From_Currency Code": "USD", "2. From_Currency Name": "United States Dollar", "3. To_Currency Code": "EUR", "4. To_Currency Name": "Euro", "5. Exchange Rate": "0.84100000", "6. Last Refreshed": "2020-08-18 03:40:01", "7. Time Zone": "UTC", "8. Bid Price": "0.84098314", "9. Ask Price": "0.84100437"}}`, a single line of JSON containing the USD-Euro Exchange Rate, Ask/Bid prices, and date/time accessed. 

Now that we've examined the API call we'll write our script to automate the call and insert it into Elasticsearch. We start with library imports.

```
import requests, json, os, logging, time
from elasticsearch import Elasticsearch
```

Now, we instantiate an "Elasticsearch" object in python from the `elasticsearch` library, which will let us communicate with our Elastic container. We use that object to create the index `forex`, under which we will insert our data. 

```es = Elasticsearch([{'host': '### YOUR APPLIANCE URL HERE ###', 'port': '9200'}])
es.indices.create(index='forex')
```

We also need to define a _mapping_ for the new index. 
This allows us to define what each of the JSON's Field Data Types should be. Although types can be assigned automatically
when inserting JSON into an index, this often leads to an unintended type being assigned to a data field - for example, the Exchange Rate being considered a string instead of a float. This would prevent the data from displaying properly on Grafana, so we define each of the JSON Field's expected types ahead of time. 

```
mapping={
            "properties":{
                "From_Currency Code":{"type": "text"},
                "From_Currency Name":{"type": "text"},
                "To_Currency Code":{"type": "text"},
                "To_Currency Name":{"type": "text"},
                "Exchange Rate":{"type": "float"},
                "Last Refreshed":{"type": "date"},
                "Time Zone":{"type": "text"},
                "Bid Price":{"type": "float"},
                "Ask Price":{"type": "float"},
                    }
                }
es.indices.put_mapping(index='forex', body=mapping)
```

We'll perform our API call via the `requests` Python library. It is set up as such:

```
API_URL = "https://www.alphavantage.co/query"
data = {
    "function": "CURRENCY_EXCHANGE_RATE",
    "from_currency": "USD",
    "to_currency": "EUR",
    "apikey": "### YOUR API KEY HERE ###",
    "datatype":"csv",
    }
    
```

We will _call_ the API inside a repeated loop, and then insert it into our index under a new ID, repeating the process indefinitely.
```
idNum = 1
while True:
    response = requests.get(API_URL, params=data)
    info = str(json.dumps(response.json()))
```
We perform three simple edits on the returned JSON in order to insert into our `forex` index properly. First, we slice off the "header"
`{"Realtime Currency Exchange Rate": ` and matching `}`
```
    info = info[36:339]
```
Then, we remove the numeric prefixes on each of our data field names. (`1. From_Currency Code` turns into `From_Currency Code`and so on.) Leaving these prefixes would cause the data to insert incorrectly, with the prefix `1. ` becoming an object containing ` From_Currency Code`, and so on for each prefix.
```
    for i in range(1,10):
        Numeral = str(i) + ". "
        info = info.replace(Numeral, "")
```
And finally we edit the `Last Refereshed` field, to change the format from `Last Refreshed": "2020-08-18 03:40:01"` into `Last Refreshed": "2020-08-19T23:03:00Z`, inserting T and Z after the data and time values. This is needed for Elasticsearch to properly parse the date/time when sorting or displaying in Grafana. 
```
    info = info[:200]+"Z"+info[200:]
    info = info[:191]+"T"+info[192:]
```
Now we insert the formatted JSON into our `forex` index, increment the ID number that it was given, and wait a little over three minutes to respect the Alphavantage API's rate limits.
```
    es.index(index='forex', ignore=400, id=idNum, body=info)
    idNum += 1
    time.sleep(200)
```

This whole script can be run with `python backgroundForex.py`. If you're inside a container, you can safely end your terminal session and the script will continue running in the background!

---
Once you have inserted the data, you can verify your success with the following commands:

`curl -X GET "### YOUR APPLIANCE URL HERE ###:9200/_cat/indices?v&pretty"` will list the container's indices. You should see that the index `forex` has been added.

`curl -X GET ### YOUR APPLIANCE URL HERE ###:9200/forex/_mapping/?pretty` This will list the fields under entries of forex - they should match our defined mapping above perfectly.

# Set up Datasources in Grafana

First, access your Grafana container via the address `http://### YOUR APPLIANCE URL HERE ###:3000` on your browser. This will first ask you to choose a username and password. When you have done this, hover over the Gear icon ("configuration") and select "Data Sources".

From this page, click the green button "Add Data Source", then click type "Elasticsearch". Enter the following settings in the setup menu:

![IMS](/forexDataSource.PNG?raw=true)

Provided that everything is working correctly, clicking the button "Save and Test" should show the message "Index OK. Time field name OK." in your Grafana window. Now that your Datasources are set up, you can load in the sample Dashboard.

# Importing the Sample Dashboard

the JSON file of the sample dashboard is in this repository. 

---
To import a new dashboard, hover over the "Four Squares" icon on Grafana, (located second from the top om the left side menu bar), and click option "Manage" to access the `Manage dashboards & folders` menu. Click on the Grey button labelled "import" on the top right of the screen. Then, either paste in the JSON data for the demo Dashboard, or download the JSON from this repository and upload it into the page via the green button labelled "Upload .json File". You will be prompted to name the dashboard, and then must accept one final confirmation dialogue to create it. 

You should see the following dashboard appear:

![IMS](/Grafana-Demo-FOREX-master/forexImage.PNG?raw=true)


If the graphs look empty, do not be alarmed! There will only be a single data point at first, with more being added every three minutes as long as the `backgroundForex` script keeps running. You'll see graphs of the USD/Euro Exchange Rate , as well as the Bid/Ask spread and the high, low, and total change inside your selected timeframe. After waiting some time for more points to appear, you can experiement with the viewed timeframe - Click on the Date to the top right of the dashboard screen and you should see a dialogue appear that lets you specify your time range. 
 
 ---
 At this point, we have Docker images of both ELK Elasticsearch and Grafana running on the zCX container, communicating with one another in order to ingest and display useful live info from outside of the appliance. 
