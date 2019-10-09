import mysql.connector
from elasticsearch import Elasticsearch
from rdflib import Namespace, URIRef, Graph
import json


cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_people', buffered=True)

cursor = cnx.cursor()
query = ("SELECT object_id, first_name,last_name FROM cb_people ")
cursor.execute(query)
map = {}

for (object_id, first_name,last_name ) in cursor:
    map[object_id] = first_name+" "+last_name


cursor.close()
cnx.close()

print map.get('p:219')

if map.get('p:0') is None:
    print "Not Found"


