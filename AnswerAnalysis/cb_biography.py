import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib


def double_quote(word):
    double_q = '"' # double quote
    return double_q + word  + double_q

g = Graph()

def fetch_biography(input_full_name):
    print "biography method"
    input_full_name = input_full_name.lower().title()
    print input_full_name

    # People.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/people.nt", format="nt")

    qres = g.query("""select ?subject {
        ?subject <http://www.crunchbased.org/people/name> """ + double_quote(input_full_name)+ """}""")

    for row in qres:
        print row

    qres = g.query("""select * {
        <http://www.crunchbased.org/people/""" + urllib.quote(input_full_name) + """> ?predicate ?object}""")

    for row in qres:
        print row

    #relationship.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/relationships.nt", format="nt")

    qres = g.query("""select ?subject {
          ?subject <http://www.crunchbased.org/relationships/person_object_id> """ + double_quote(input_full_name) + """}""")

    rowIdArray = []
    subjects = []
    for row in qres:
        print row
        subject = row[0]
        rowId = row[0].split("/")[-1]
        rowIdArray.append(rowId)
        subjects.append(subject)

    for index, elem in enumerate(rowIdArray):
        qres = g.query("""select * {
            <http://www.crunchbased.org/relationships/""" + elem + """> ?predicate ?object}""")

        for row in qres:
            print row


    #degrees.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/degrees.nt", format="nt")

    qres = g.query("""select ?subject {
              ?subject <http://www.crunchbased.org/degrees/object_id> """ + double_quote(
        input_full_name) + """}""")

    rowIdArray = []
    subjects = []
    for row in qres:
        print row
        subject = row[0]
        rowId = row[0].split("/")[-1]
        rowIdArray.append(rowId)
        subjects.append(subject)

    for index, elem in enumerate(rowIdArray):
        qres = g.query("""select * {
                <http://www.crunchbased.org/relationships/""" + elem + """> ?predicate ?object}""")

        for row in qres:
            print row




def fetch_history(input_full_name):
    print "History Method"