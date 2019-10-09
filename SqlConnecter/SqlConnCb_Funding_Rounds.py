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
                              database='cb_funding_rounds')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_funding_rounds")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()


hostname = "http://www.crunchbased.org/fundingRounds/"
hostFundingRoundId = hostname + "funding_round_id"
hostObjectId =  hostname + "object_id"
hostFundingRoundType =  hostname + "funding_round_type"
hostRoundCode = hostname + "funding_round_code"
hostRaisedAmount = hostname + "raised_amount"
hostSourceUrl = hostname + "source_url"
hostSourceDescription = hostname + "source_descrption"


counter = 0
columValues = []
print "Starting loop"
row = cursor.fetchone()

while row is not None:
    for c in row:
        columValues.append(c)


    subject = rdflib.term.URIRef(hostname + str(columValues[0]))

    #    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateAcquistionsId = rdflib.term.URIRef(hostFundingRoundId)
    g.add((subject, predicateAcquistionsId, Literal(columValues[1])))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateAcquiringId = rdflib.term.URIRef(hostObjectId)
    g.add((subject, predicateAcquiringId, Literal(map.get(columValues[2]))))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateAcquiredId = rdflib.term.URIRef(hostFundingRoundType)
    g.add((subject, predicateAcquiredId, Literal(columValues[4])))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateTermCode = rdflib.term.URIRef(hostRoundCode)
    g.add((subject, predicateTermCode, Literal(columValues[7])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateAcquiredAt = rdflib.term.URIRef(hostRaisedAmount)
    g.add((subject, predicateAcquiredAt, Literal(columValues[8])))
    # predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
    predicateSourceUrl = rdflib.term.URIRef(Literal(hostSourceUrl))
    g.add((subject , predicateSourceUrl, Literal(columValues[19])))

    predicateSourceDescription = rdflib.term.URIRef(Literal(hostSourceDescription))
    g.add((subject, predicateSourceDescription, Literal(columValues[20])))

    columValues = []
    counter +=1;
    row = cursor.fetchone()

print "Number of Records are {}".format(counter)
cursor.close()
cnx.close()

print "Serialization"
s = g.serialize(format='nt')
print "Write Data to file"
outfile = open("funding_round.nt","w")
outfile.write(s)