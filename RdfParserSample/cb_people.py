import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib
g = Graph()

# http://www.slideshare.net/alchueyr/getting-the-most-out-of-sparql-with-python

#http://stackoverflow.com/questions/2760896/how-can-one-extract-rdfabout-or-rdfid-properties-from-triples-using-sparql
"""
import os
print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

print("This file directory only")
print(os.path.dirname(full_path))


g.parse("./CrunchBasedPlayGround/SqlConnecter/people.nt", format="nt")
#g.parse("people.nt", format="nt")
"""

input_var = raw_input("Enter something: ")
print ("you entered " + input_var)


# Copy the Name
name = input_var

def double_quote(word):
    double_q = '"' # double quote
    return double_q + word + double_q

first_name = double_quote(name)


qres = g.query("""select ?subject {
    ?subject <http://www.crunchbased.org/people/name> """+first_name+"""}""")


rowId = None;
subject = None
for row in qres:
    print row
    subject = row[0]
    rowId = row[0].split("/")[-1]


print "Row Id is {}".format(rowId)

qres = g.query("""select * {
    <http://www.crunchbased.org/people/"""+urllib.quote(name)+"""> ?predicate ?object}""")

predicate = None
obj = None

file = open('{0}.txt'.format(name),"w")
#file = open("newfile.txt", "w")

for row in qres:
    print row
    predicate = row [1]
    obj = row [0]
    file.write(subject)
    file.write("\t")
    file.write(predicate)
    file.write("\t")
    file.write(obj)
    file.write("\n")



#for subject,predicate,obj in g:
#    print subject , predicate ,obj

