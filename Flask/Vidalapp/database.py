from .views import app
import logging as lg

from pymongo import MongoClient

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class MongoDB():
    def __init__(self):
        self.client = MongoClient()
        self.db = client['Vidal']

class ElasticsearchDB():
    LOCAL = True
    def __init__(self):
        self.mongo = MongoDB()
        self.client = Elasticsearch(hosts=["localhost" if LOCAL else "elasticsearch"])
        bulk(self.client, self.index_mongo('substance_items'))
        #bulk(self.client, self.index_mongo('Medicament_Items'))

    def index_mongo(self, index):
        cursor = list(self.mongo.db[index].find())
        for item in cursor:
            _id = str(item['_id'])
            del item['_id']
            document = {
                "_index" : index,
                "_type"  : index+"_document",
                "_id"    : _id,
                "_source": item
            }
            yield document

def init_db():
    elastic = ElasticsearchDB()