import mysql.connector
from rdflib import Namespace, URIRef, Graph , Literal
from rdflib.namespace import RDF, FOAF
import rdflib


# http://www.mysqltutorial.org/python-mysql-query/
# http://stackoverflow.com/questions/409705/mysql-selecting-data-from-multiple-tables-all-with-same-structure-but-differen



cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_funds')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_funds")
cursor.execute(query)

g = Graph()

hostname = "http://www.crunchbased.org/funds/"
hostFundId = hostname + "fund_id"
hostObjectId =  hostname + "object_id"
hostFundName =  hostname + "name"
hostFundedAt= hostname + "funded_at"
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
    predicateFundId = rdflib.term.URIRef(hostFundId)
    g.add((subject, predicateFundId, Literal(columValues[1])))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateObjectId = rdflib.term.URIRef(hostObjectId)
    g.add((subject, predicateObjectId, Literal(columValues[2])))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateFundName = rdflib.term.URIRef(hostFundName)
    g.add((subject, predicateFundName, Literal(columValues[3])))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateFundedAt = rdflib.term.URIRef(hostFundedAt)
    g.add((subject, predicateFundedAt, Literal(columValues[4])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateRaisedAmount = rdflib.term.URIRef(hostRaisedAmount)
    g.add((subject, predicateRaisedAmount, Literal(columValues[5])))
    # predicateEntityCountryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/country_code")
    predicateSourceUrl = rdflib.term.URIRef(Literal(hostSourceUrl))
    g.add((subject , predicateSourceUrl, Literal(columValues[7])))

    predicateSourceDescription = rdflib.term.URIRef(Literal(hostSourceDescription))
    g.add((subject, predicateSourceDescription, Literal(columValues[8])))

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
outfile = open("funds.nt","w")
outfile.write(s)