import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON

g = Graph()

# http://www.slideshare.net/alchueyr/getting-the-most-out-of-sparql-with-python

#http://stackoverflow.com/questions/2760896/how-can-one-extract-rdfabout-or-rdfid-properties-from-triples-using-sparql


g.parse("./CrunchBasedPlayGround/SqlConnecter/objects.nt", format="nt")
#g.parse("people.nt", format="nt")

name = "Ben Elowitz"
file = open('{0}.txt'.format(name),"a+")
#file = open("newfile.txt", "w")
objlist = ["c:1","c:4993","c:233024","c:1017","c:18661","c:537","c:2361","c:268504"]

def double_quote(word):
    double_q = '"' # double quote
    return double_q + word + double_q


for id in objlist:
    input_object_id = id

    qres = g.query("""select * {
            <http://www.crunchbased.org/objects/""" + input_object_id + """> ?predicate ?object}""")


    for row in qres:
        print row
        subject = "http://www.crunchbased.org/objects/"+input_object_id
        obj = row[0]
        predicate = row [1]
        file.write(subject)
        file.write("\t")
        file.write(predicate)
        file.write("\t")
        file.write(obj)
        file.write("\n")

file.close()

#for subject,predicate,obj in g:
#    print subject , predicate ,obj