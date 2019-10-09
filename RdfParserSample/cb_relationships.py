import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON

g = Graph()

# http://www.slideshare.net/alchueyr/getting-the-most-out-of-sparql-with-python

#http://stackoverflow.com/questions/2760896/how-can-one-extract-rdfabout-or-rdfid-properties-from-triples-using-sparql


g.parse("./CrunchBasedPlayGround/SqlConnecter/relationships.nt", format="nt")
#g.parse("people.nt", format="nt")

input_var = raw_input("Enter something: ")
print ("you entered " + input_var)

def double_quote(word):
    double_q = '"' # double quote
    return double_q + word + double_q

input_object_id = double_quote(input_var)

qres = g.query("""select ?subject {
    ?subject <http://www.crunchbased.org/relationships/person_object_id> """+input_object_id+"""}""")


name = "Ben Elowitz"
file = open('{0}.txt'.format(name),"a+")
#file = open("newfile.txt", "w")

rowIdArray = []
subjects = []
for row in qres:
    print row
    subject = row[0]
    rowId = row[0].split("/")[-1]
    rowIdArray.append(rowId)
    subjects.append(subject)


print len(rowIdArray)

for rowId in rowIdArray:
    print rowId

for index, elem in enumerate(rowIdArray):
    qres = g.query("""select * {
        <http://www.crunchbased.org/relationships/"""+elem+"""> <http://www.crunchbased.org/relationships/relationship_object_id> ?object}""")

    predicate = None
    obj = None

    for row in qres:
        print row
        predicate = "http://www.crunchbased.org/relationships/relationship_object_id"
        obj = row [0]
        file.write(subjects[index])
        file.write("\t")
        file.write(predicate)
        file.write("\t")
        file.write(obj)
        file.write("\n")

file.close()

#for subject,predicate,obj in g:
#    print subject , predicate ,obj