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
                              database='cb_funds', buffered=True)

cursor = cnx.cursor()
query = ("SELECT object_id,name FROM cb_funds ")
cursor.execute(query)
fundMap = {}

for (object_id, name ) in cursor:
    fundMap[object_id.encode('ascii','ignore')] = name



cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_objects', buffered=True)

cursor = cnx.cursor()
query = ("SELECT id, name FROM cb_objects ")
cursor.execute(query)
cpyMap = {}

for (id, normalized_name  ) in cursor:
    cpyMap[id.encode('ascii','ignore')] = name

cursor.close()
cnx.close()



cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_investments')

cursor = cnx.cursor()
query = ("SELECT id, funding_round_id, funded_object_id, investor_object_id FROM cb_investments")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()

hostname = "http://www.crunchbased.org/investments/"
hostFundingRoundId = hostname + "funding_round_id"
hostFundedId =  hostname + "funded_object_id"
hostInvestorObjectId =  hostname + "investor_object_id"

counter = 0
for (id, funding_round_id, funded_object_id, investor_object_id) in cursor:

#  print "{}, {} decription is {}".format(entity_type, name, description)
    subject = rdflib.term.URIRef(hostname+ str(id))

#    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateEntityType = rdflib.term.URIRef(hostFundingRoundId)
    g.add((subject , predicateEntityType, Literal(funding_round_id)))
#    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateEntityId = rdflib.term.URIRef(hostFundedId)

    funded_object_id_value = None
    if cpyMap.get(funded_object_id) is not None:
        funded_object_id_value = cpyMap.get(funded_object_id)
    if pplMap.get(funded_object_id) is not None:
        funded_object_id_value = pplMap.get(funded_object_id)

    g.add((subject , predicateEntityId, Literal(funded_object_id_value)))
#    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateEntityName = rdflib.term.URIRef(hostInvestorObjectId)
    g.add((subject , predicateEntityName, Literal(fundMap.get(investor_object_id))))

    counter += 1

print "Number of Records are {}".format(counter)
cursor.close()
cnx.close()


print "Serialization"
s = g.serialize(format='nt')
print "Write Data to file"
outfile = open("investments.nt","w")
outfile.write(s)