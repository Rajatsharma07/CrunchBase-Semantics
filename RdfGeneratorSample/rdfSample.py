from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib
# https://www.youtube.com/watch?v=5DCS9LE-8rE

g = Graph()
subject = rdflib.term.URIRef("http://www.example.org/cb_objects/c:1")
predicate = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
g.add((subject , predicate, Literal("Company")))


predicate = rdflib.term.URIRef("http://www.example.org/cb_objects/name")
g.add((subject , predicate, Literal('WetName')))

subject = rdflib.term.URIRef("http://www.example.org/cb_objects/c:2")
predicate = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
g.add((subject , predicate, Literal('Company')))

s = g.serialize(format='pretty-xml')
outfile = open("test.xml","w")
outfile.write(s)