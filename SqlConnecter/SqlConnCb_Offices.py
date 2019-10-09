import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib

# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen

cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects', buffered=True)

cursor = cnx.cursor()
query = ("SELECT id, name FROM cb_objects ")
cursor.execute(query)
map = {}

for (id, name  ) in cursor:
    map[id.encode('ascii','ignore')] = name


cursor.close()
cnx.close()

cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_relationships')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_offices")

cursor.execute(query)

g = Graph()

hostname = "http://www.crunchbased.org/offices/"
hostObjectId = hostname + "object_id"
hostOfficeId = hostname + "office_id"
hostDescriptionId =  hostname + "description"
hostRegion =  hostname + "region"
hostAddress1 = hostname + "address1"
hostAddress2 = hostname + "address2"
hostCity = hostname + "city"
hostZipCode = hostname + "zip_code"
hostStateCode = hostname + "state_code"
hostCountryCode = hostname + "country_code"
hostLatitude = hostname + "latitude"
hostLongitude = hostname + "longitude"


counter = 0
columValues = []
print "Starting loop"
row = cursor.fetchone()

while row is not None:
    for c in row:
        columValues.append(c)


    subject = rdflib.term.URIRef(hostname + str(columValues[0]))

    #    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateObjectId = rdflib.term.URIRef(hostObjectId)

    g.add((subject, predicateObjectId, Literal(map.get(columValues[1]))))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateOfficeId = rdflib.term.URIRef(hostOfficeId)
    g.add((subject, predicateOfficeId, Literal(columValues[2])))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateDescription = rdflib.term.URIRef(hostDescriptionId)
    g.add((subject, predicateDescription, Literal(columValues[3])))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateRegion = rdflib.term.URIRef(hostRegion)
    g.add((subject, predicateRegion, Literal(columValues[4])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateAddress1 = rdflib.term.URIRef(hostAddress1)
    g.add((subject, predicateAddress1, Literal(columValues[5])))
    # predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
    predicateAddress2 = rdflib.term.URIRef(Literal(hostAddress2))
    g.add((subject , predicateAddress2, Literal(columValues[7])))

    predicateHostCity = rdflib.term.URIRef(Literal(hostCity))
    g.add((subject, predicateHostCity, Literal(columValues[8])))

    predicateZipCode = rdflib.term.URIRef(hostZipCode)
    g.add((subject, predicateZipCode, Literal(columValues[9])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateStateCode = rdflib.term.URIRef(hostStateCode)
    g.add((subject, predicateStateCode , Literal(columValues[10])))
    # predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
    predicateCountryCode = rdflib.term.URIRef(Literal(hostCountryCode))
    g.add((subject, predicateCountryCode, Literal(columValues[11])))

    predicateLatitude = rdflib.term.URIRef(Literal(hostLatitude))
    g.add((subject, predicateLatitude, Literal(columValues[12])))

    predicateLongitude = rdflib.term.URIRef(Literal(hostLongitude))
    g.add((subject, predicateLongitude , Literal(columValues[13])))

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
outfile = open("offices.nt","w")
outfile.write(s)