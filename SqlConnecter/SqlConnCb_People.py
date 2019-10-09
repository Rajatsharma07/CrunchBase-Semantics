import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib
import urllib
# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen
cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_people')

cursor = cnx.cursor()
query = ("SELECT id, object_id, first_name, last_name, birthplace, affiliation_name FROM cb_people")

cursor.execute(query)
#data = cursor.fetchall()


g = Graph()

hostname = "http://www.crunchbased.org/people/"
hostObjectId = hostname + "object_id"
hostName =  hostname + "name"
hostLastName =  hostname + "last_name"
hostBirthPlace = hostname + "birthplace"
hostAffliattionName = hostname + "affliation_name"

counter = 0
for (id, object_id, first_name, last_name, birthplace, affiliation_name) in cursor:
#  print "{}, {} decription is {}".format(entity_type, name, description)

#    subject = rdflib.term.URIRef(hostname+ str(first_name.encode('ascii','ignore').replace("20%"," ")+"20%"+last_name.encode('ascii','ignore').replace("20%"," ")))
    subject = rdflib.term.URIRef(hostname + urllib.quote(first_name.encode('ascii', 'ignore')+ " " + last_name.encode('ascii', 'ignore')))

#    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateObjectId = rdflib.term.URIRef(hostObjectId)
    g.add((subject , predicateObjectId, Literal(object_id)))
#    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateFirstName = rdflib.term.URIRef(hostName)
    g.add((subject , predicateFirstName, Literal(first_name+" "+last_name)))
#    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
#    predicateLastName = rdflib.term.URIRef(hostLastName)
#    g.add((subject , predicateLastName, Literal(last_name)))
#    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateBirthPlace = rdflib.term.URIRef(hostBirthPlace)
    g.add((subject , predicateBirthPlace, Literal(birthplace)))
#    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateAffiliationName = rdflib.term.URIRef(hostAffliattionName)
    g.add((subject , predicateAffiliationName, Literal(affiliation_name)))

    counter += 1

print "Number of Records are {}".format(counter)
cursor.close()
cnx.close()


print "Serialization"
s = g.serialize(format='nt')
print "Write Data to file"
outfile = open("people.nt","w")
outfile.write(s)