import requests, json, os, logging, time
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': '### YOUR APPLIANCE URL HERE ###', 'port': '9200'}])
es.indices.create(index='forex')
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
API_URL = "https://www.alphavantage.co/query"
data = {
    "function": "CURRENCY_EXCHANGE_RATE",
    "from_currency": "USD",
    "to_currency": "EUR",
    "apikey": "### YOUR API KEY HERE ###",
    "datatype":"csv",
    }
idNum = 1
while True:
    response = requests.get(API_URL, params=data)
    info = str(json.dumps(response.json()))
    info = info[36:339]
    for i in range(1,10):
        Numeral = str(i) + ". "
        info = info.replace(Numeral, "")
    info = info[:200]+"Z"+info[200:]
    info = info[:191]+"T"+info[192:]
    es.index(index='forex', ignore=400, id=idNum, body=info)
    idNum += 1
    time.sleep(200)