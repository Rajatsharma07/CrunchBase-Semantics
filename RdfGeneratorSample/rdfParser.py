import rdflib
from rdflib import Namespace, URIRef, Graph
g = Graph()

g.parse("test.xml", format="xml")

for subject,predicate,obj in g:
    print subject , predicate ,obj


#g.serialize("test.rdf", format="pretty-xml")