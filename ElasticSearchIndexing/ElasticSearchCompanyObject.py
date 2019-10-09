
from elasticsearch import Elasticsearch
from rdflib import Namespace, URIRef, Graph
import json

es = Elasticsearch()

index_name =  "crunchbased"
index_type = "crunchbasedtype"

if es.indices.exists(index_name):
    print "Index Exist"
else:
    print "Creating Index"
    es.indices.create(index=index_name)

g = Graph()

g.parse("./CrunchBasedPlayGround/SqlConnecter/objectsTwo.nt", format="nt")

qres = g.query("""select ?subject ?predicate ?object {
    ?subject ?predicate ?object
}""")

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

    json_data = json.dumps(data)
    res = es.index(index=index_name, doc_type=index_type, body=json_data)
    if counter % 100000 == 0:
        print counter



es.indices.refresh(index=index_name)
print "Indexing Done"
    #doc = {
#    'author': 'kimchy',
#    'text': 'Elasticsearch: cool. bonsai cool.',
#    'timestamp': datetime.now(),
#
#res = es.index(index="crunch-based", doc_type='cbdata',body=doc)
#print(res['created'])

#res = es.get(index="test-index", doc_type='tweet', id=1)
#print(res['_source'])

#es.indices.refresh(index="test-index")

#res = es.search(index="test-index", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])



#print helpers.bulk(es, data)