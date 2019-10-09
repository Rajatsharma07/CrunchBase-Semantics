import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib

# https://www.w3.org/TR/rdb-direct-mapping/
# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen
cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects')

cursor = cnx.cursor()
query = ("SELECT id, entity_type, name, twitter_username, category_code, country_code FROM cb_objects")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()

hostname = "http://www.crunchbased.org/objects/"
hostEntityType = hostname + "entity_type"
hostEntityId =  hostname + "entity_id"
hostEntityName =  hostname + "name"
hostEntityCategoryCode = hostname + "category_code"
hostEntityTwitter = hostname + "twitter_username"
hostEntityCountryCode = hostname + "country_code"

counter = 0
for (id, entity_type, entity_id, name, twitter_username, category_code) in cursor:
#  print "{}, {} decription is {}".format(entity_type, name, description)
    subject = rdflib.term.URIRef(hostname+id)

#    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateEntityType = rdflib.term.URIRef(hostEntityType)
    g.add((subject , predicateEntityType, Literal(entity_type)))
#    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateEntityId = rdflib.term.URIRef(hostEntityId)
    g.add((subject , predicateEntityId, Literal(entity_id)))
#    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateEntityName = rdflib.term.URIRef(hostEntityName)
    g.add((subject , predicateEntityName, Literal(name)))
#    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateEntityCategoryCode = rdflib.term.URIRef(hostEntityCategoryCode)
    g.add((subject , predicateEntityCategoryCode, Literal(category_code)))
#    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateEntityTwitterUsername = rdflib.term.URIRef(hostEntityTwitter)
    g.add((subject , predicateEntityTwitterUsername, Literal(twitter_username)))
#    predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
#    predicateEntityCountryCode = rdflib.term.URIRef(Literal(hostEntityCountryCode))
#    g.add((subject , predicateEntityCountryCode, Literal(country_code)))

    counter += 1

print "Number of Records are {}".format(counter)
cursor.close()
cnx.close()

print "Serialization"
s = g.serialize(format='nt')
print "Write Data to file"
outfile = open("objects.nt","w")
outfile.write(s)