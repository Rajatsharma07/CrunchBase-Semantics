import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON

g = Graph()

# http://www.slideshare.net/alchueyr/getting-the-most-out-of-sparql-with-python

#http://stackoverflow.com/questions/2760896/how-can-one-extract-rdfabout-or-rdfid-properties-from-triples-using-sparql


g.parse("./CrunchBasedPlayGround/SqlConnecter/milestones.nt", format="nt")
#g.parse("people.nt", format="nt")

#file = open("newfile.txt", "w")
objlist = ["c:1","c:4993","c:233024","c:1017","c:18661","c:537","c:2361","c:268504"]

name = "Ben Elowitz"
file = open('{0}.txt'.format(name), "a+")

def double_quote(word):
    double_q = '"' # double quote
    return double_q + word + double_q


for getId in objlist:

    input_object_id = double_quote(getId)

    qres = g.query("""select ?subject {
        ?subject <http://www.crunchbased.org/milestones/object_id> """+input_object_id+"""}""")



    #file = open("newfile.txt", "w")

    rowIdArray = []
    subjects = []
    for row in qres:
        print row
        subject = row[0]
        rowId = row[0].split("/")[-1]
        rowIdArray.append(rowId)
        subjects.append(subject)

    for rowId in rowIdArray:
        print rowId

    for index, elem in enumerate(rowIdArray):
        qres = g.query("""select * {
            <http://www.crunchbased.org/milestones/"""+elem+"""> ?predicate ?object}""")

        predicate = None
        obj = None

        for row in qres:
            print row
            predicate = row[1]
            obj = row [0]
            file.write(subjects[index])
            file.write("\t")
            file.write(predicate)
            file.write("\t")
            file.write(obj.encode("utf-8"))
            file.write("\n")

file.close()

#for subject,predicate,obj in g:
#    print subject , predicate ,obj