import mysql.connector
from elasticsearch import Elasticsearch
from rdflib import Namespace, URIRef, Graph
import json


cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects', buffered=True)

cursor = cnx.cursor()
query = ("SELECT id, normalized_name FROM cb_objects ")
cursor.execute(query)
map = {}

for (id, normalized_name  ) in cursor:
    map[id.encode('ascii','ignore')] = normalized_name


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

g.parse("./CrunchBasedPlayGround/SqlConnecter/acquisitions.nt", format="nt")

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


    if 'acquiring_object_id' in predicate:
#        print predicate
#        print type(str(object.toPython()))
        object = str(object.toPython())
#        print object
        if map.get(object) is not None:
            data['object'] = map.get(object)
#            print data.get('object')

    if 'acquired_object_id' in predicate:
        #        print predicate
        #        print type(str(object.toPython()))
        object = str(object.toPython())
        #        print object
        if map.get(object) is not None:
            data['object'] = map.get(object)
        #            print data.get('object')

    json_data = json.dumps(data)
    res = es.index(index=index_name, doc_type=index_type, body=json_data)
    if counter % 100000 == 0:
        print counter


es.indices.refresh(index=index_name)
print "Indexing Done"
