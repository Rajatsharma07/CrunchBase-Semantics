import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib

# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen

cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_people', buffered=True)

cursor = cnx.cursor()
query = ("SELECT object_id, first_name,last_name FROM cb_people ")
cursor.execute(query)
pplMap = {}

for (object_id, first_name,last_name ) in cursor:
    pplMap[object_id.encode('ascii','ignore')] = first_name +" "+ last_name



cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects', buffered=True)

cursor = cnx.cursor()
query = ("SELECT id, normalized_name FROM cb_objects ")
cursor.execute(query)
cpyMap = {}

for (id, name  ) in cursor:
    cpyMap[id.encode('ascii','ignore')] = name

cursor.close()
cnx.close()


cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_relationships')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_relationships")

cursor.execute(query)

g = Graph()

hostname = "http://www.crunchbased.org/relationships/"
hostRelationshipId = hostname + "realtionship_id"
hostPersonObjectId = hostname + "person_object_id"
hostRelationshipObjectId =  hostname + "relationship_object_id"
hostStart =  hostname + "start_at"
hostEnd = hostname + "end_at"
hostpast = hostname + "is_past"
hostSequence = hostname + "sequence"
hostTitle = hostname + "title"

counter = 0
columValues = []
print "Starting loop"
row = cursor.fetchone()


while row is not None:
    for c in row:
        columValues.append(c)


    subject = rdflib.term.URIRef(hostname + str(columValues[0]))

    #    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateObjectId = rdflib.term.URIRef(hostRelationshipId)
    g.add((subject, predicateObjectId, Literal(columValues[1])))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateOfficeId = rdflib.term.URIRef(hostPersonObjectId)
    g.add((subject, predicateOfficeId, Literal(pplMap.get(columValues[2]))))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateDescription = rdflib.term.URIRef(hostRelationshipObjectId)
    g.add((subject, predicateDescription, Literal(cpyMap.get(columValues[3]))))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateRegion = rdflib.term.URIRef(hostStart)
    g.add((subject, predicateRegion, Literal(columValues[4])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateAddress1 = rdflib.term.URIRef(hostEnd)
    g.add((subject, predicateAddress1, Literal(columValues[5])))
    # predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
    predicateAddress2 = rdflib.term.URIRef(Literal(hostpast))
    g.add((subject , predicateAddress2, Literal(columValues[7])))

    predicateHostCity = rdflib.term.URIRef(Literal(hostSequence))
    g.add((subject, predicateHostCity, Literal(columValues[8])))

    predicateZipCode = rdflib.term.URIRef(hostTitle)
    g.add((subject, predicateZipCode, Literal(columValues[9])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username"
    columValues = []
    counter +=1;
    row = cursor.fetchone()

#data = cursor.fetchall()



print "Number of Records are {}".format(counter)
cursor.close()
cnx.close()


print "Serialization"
s = g.serialize(format='nt')
print "Write Data to file"
outfile = open("relationships.nt","w")
outfile.write(s)