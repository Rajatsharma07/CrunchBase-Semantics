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
map = {}

for (object_id, first_name,last_name ) in cursor:
    map[object_id.encode('ascii','ignore')] = first_name +" "+ last_name


cursor.close()
cnx.close()

cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_degrees')

cursor = cnx.cursor()
query = ("SELECT id, object_id, degree_type, subject, institution, graduated_at FROM cb_degrees")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()

hostname = "http://www.crunchbased.org/degrees/"
hostObjectId = hostname + "object_id"
hostDegreeType =  hostname + "degree_type"
hostSubject =  hostname + "subject"
hostInstitution = hostname + "institution"
hostGraduatedAt = hostname + "graduated_at"

counter = 0
for (id, object_id, degree_type, subject, institution, graduated_at) in cursor:

    subjectGlobal = rdflib.term.URIRef(hostname + str(id))

    #    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateObjectType = rdflib.term.URIRef(hostObjectId)
    g.add((subjectGlobal, predicateObjectType, Literal(map.get(object_id))))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateDegree = rdflib.term.URIRef(hostDegreeType)
    g.add((subjectGlobal, predicateDegree, Literal(degree_type)))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateSubject = rdflib.term.URIRef(hostSubject)
    g.add((subjectGlobal, predicateSubject, Literal(subject)))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateInstitution = rdflib.term.URIRef(hostInstitution)
    g.add((subjectGlobal, predicateInstitution, Literal(institution)))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateGraduation = rdflib.term.URIRef(hostGraduatedAt)

    if graduated_at is not None:
        g.add((subjectGlobal, predicateGraduation, Literal(str(graduated_at)[0:4])))
    else:
        g.add((subjectGlobal, predicateGraduation, Literal(graduated_at)))

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
outfile = open("degrees.nt","w")
outfile.write(s)