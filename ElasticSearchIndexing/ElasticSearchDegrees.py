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
    map[object_id.encode('ascii','ignore')] = first_name +" "+ last_name


cursor.close()
cnx.close()

#for key, value in map.iteritems() :
#    print type(key), type(value.encode('ascii','ignore'))

es = Elasticsearch()

index_name =  "crunch-based"
index_type = "crunchbasedtype"

if es.indices.exists(index_name):
    print "Index Exist"
else:
    print "Creating Index"
    es.indices.create(index=index_name)

g = Graph()

g.parse("./CrunchBasedPlayGround/SqlConnecter/degrees.nt", format="nt")

qres = g.query("""select ?subject ?predicate ?object {
    ?subject ?predicate ?object
}""")

print "Start"
counter = 0
for subject, predicate, object in qres:
#    print subject
    counter = counter + 1
    data = {}
    data['subject']        =  subject
    data['subjectUrl']     =  subject[0 : subject.rindex("/")]
    data['subjectValue']   =  subject[ subject.rindex("/") +1 : ]
    data['predicate']      =  predicate
    data['predicateteUrl'] =  predicate[0 : predicate.rindex("/")]
    data['predicateValue'] =  predicate[ predicate.rindex("/") + 1 : ]
    data['object']         =  object

    if 'graduated_at' in predicate:
#        print predicate
#        print object
        if object is not None:
            data['object'] =  object[0:4]

    if 'object_id' in predicate:
#        print object
#        print predicate
#        print type(str(object.toPython()))
        object = str(object.toPython())
#        print object
        if map.get(object) is not None:
            data['object'] = map.get(object)
            print data.get('object')




    json_data = json.dumps(data)
    res = es.index(index=index_name, doc_type=index_type, body=json_data)
    if counter % 100000 == 0:
        print counter


es.indices.refresh(index=index_name)
print "Indexing Done"
