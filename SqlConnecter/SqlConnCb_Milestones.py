import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib

# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen
cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_milestones')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_milestones")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()

hostname = "http://www.crunchbased.org/milestones/"
hostObjectId =  hostname + "object_id"
hostMilestoneAt = hostname + "milestone_at"
hostMilestoneCode =  hostname + "milestone_code"
hostDescription = hostname + "description"
hostSourceUrl = hostname + "source_url"
hostSourceDescription = hostname + "source_description"

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
    g.add((subject, predicateObjectId, Literal(columValues[1])))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateMilesstoneAt = rdflib.term.URIRef(hostMilestoneAt)
    g.add((subject, predicateMilesstoneAt, Literal(columValues[2])))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateMilestoneCode = rdflib.term.URIRef(hostMilestoneCode)
    g.add((subject, predicateMilestoneCode, Literal(columValues[3])))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateDescription = rdflib.term.URIRef(hostDescription)
    g.add((subject, predicateDescription, Literal(columValues[4])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateSourceUrl = rdflib.term.URIRef(hostSourceUrl)
    g.add((subject, predicateSourceUrl, Literal(columValues[5])))

    predicateSourceDescription = rdflib.term.URIRef(hostSourceDescription)
    g.add((subject, predicateSourceDescription, Literal(columValues[6])))

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
outfile = open("milestones.nt","w")
outfile.write(s)