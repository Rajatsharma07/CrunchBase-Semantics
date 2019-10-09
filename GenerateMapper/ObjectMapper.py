import csv
import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal

try:
    import json
except ImportError:
    import simplejson as json

# SQL Connection
cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects')

cursor = cnx.cursor()
query = ("SELECT id, normalized_name FROM cb_objects")

cursor.execute(query)

# Csv File

csvfile = open('mapper.csv','wb')
mywriter = csv.writer(csvfile)

#mywriter.writerows([("ObjectId","Value")])
# .encode('ascii','ignore'
#id.encode('ascii','ignore')

for (id, normalized_name) in cursor:
    print (id)
    print (normalized_name)
#    mywriter.writerows([id.encode('ascii','ignore')])


# Close CSV File
csvfile.close()

# Close SQL Connection
cursor.close()
cnx.close()