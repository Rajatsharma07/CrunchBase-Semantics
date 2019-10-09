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
cpyMap = {}

for (id, name  ) in cursor:
    cpyMap[id.encode('ascii','ignore')] = name

cursor.close()
cnx.close()

cnx = mysql.connector.connect(user='root', password='rajat',
                              host='127.0.0.1',
                              database='cb_ipos')

cursor = cnx.cursor()
query = ("SELECT * FROM cb_ipos")

cursor.execute(query)
#data = cursor.fetchall()

g = Graph()

hostname = "http://www.crunchbased.org/ipos/"
hostIpoId = hostname + "ipo_id"
hostObjectId =  hostname + "object_id"
hostValuationAmount =  hostname + "valuation_amount"
hostStockSymbol= hostname + "stock_symbol"
hostPublicAt = hostname + "public_at"

counter = 0
columValues = []
print "Starting loop"
row = cursor.fetchone()


while row is not None:
    for c in row:
        columValues.append(c)


    subject = rdflib.term.URIRef(hostname + str(columValues[0]))

    #    predicateEntityType = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_type")
    predicateFundId = rdflib.term.URIRef(hostIpoId)
    g.add((subject, predicateFundId, Literal(columValues[1])))
    #    predicateEntityId = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateObjectId = rdflib.term.URIRef(hostObjectId)

    g.add((subject, predicateObjectId, Literal(cpyMap.get(columValues[2]))))
    #    predicateEntityname = rdflib.term.URIRef("http://www.example.org/cb_objects/entity_id")
    predicateFundName = rdflib.term.URIRef(hostValuationAmount)
    g.add((subject, predicateFundName, Literal(columValues[3])))
    #    predicateEntityCategoryCode = rdflib.term.URIRef("http://www.example.org/cb_objects/category_code")
    predicateFundedAt = rdflib.term.URIRef(hostStockSymbol)
    g.add((subject, predicateFundedAt, Literal(columValues[8])))
    #    predicateEntityTwitterUsername = rdflib.term.URIRef("http://www.example.org/cb_objects/twitter_username")
    predicateRaisedAmount = rdflib.term.URIRef(hostPublicAt)
    g.add((subject, predicateRaisedAmount, Literal(columValues[7])))

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
outfile = open("ipos.nt","w")
outfile.write(s)