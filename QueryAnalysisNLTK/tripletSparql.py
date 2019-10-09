import rdflib
from rdflib import Namespace, URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib


def double_quote(word):
    double_q = '"' # double quote
    return double_q + word  + double_q

g = Graph()

def fetch_peoples(input_full_name):

    input_full_name = input_full_name.lower().title()
    print input_full_name

    # People.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/people.nt", format="nt")

    qres = g.query("""select * {
        <http://www.crunchbased.org/people/""" + urllib.quote(input_full_name) + """> ?predicate ?object .
        ?subject ?predicate """ + double_quote(input_full_name)+ """ . }""")

    for row in qres:
        print row
        print row[0]
        print row[1]
        print row[2]


def fetch_relationship_org(input_full_Org , gen_word):

    orgTupList = []
    orgIdList = []
    genTupList = []
    genIdList = []

    # People.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/relationships.nt", format="nt")

    qres = g.query("""select * {
        ?subject ?predicate """ + double_quote(input_full_Org)+ """ . }""")

    for row in qres:

        rowId = row[1].split("/")[-1]
        tup = (rowId, input_full_Org)
#        print int(rowId)
        orgIdList.append(int(rowId))
        orgTupList.append(tup)


    for word in gen_word:

        qres = g.query("""select * {
                ?subject ?predicate """ + double_quote(word) + """ . }""")


        for row in qres:

            rowId = row[1].split("/")[-1]
            tup = (rowId, word)
            genIdList.append(int(rowId))
            genTupList.append(tup)


    matched_list =  []


    for num in orgIdList:

        if num in genIdList:

            matched_list.append(num)


#    print len(matched_list)

    counter = 0
    for elem in (matched_list):
        subject = "http://www.crunchbased.org/relationships/{}".format(str(elem))
        qres = g.query("""select * {
                <http://www.crunchbased.org/relationships/""" + str(elem) + """> ?predicate ?object}""")


        for row in qres:
            print row[0] , row[1] , subject

            if (row[0].toPython()) in gen_word:
                counter = gen_word.index(row[0].toPython())


        print "Rank is {}".format(counter)
        print " "


def fetch_graduates(input_university , input_year, gen_word):

    yrList   = []
    university_list = []
    # Degrees.nt
    g.parse("./CrunchBasedPlayGround/SqlConnecter/degrees.nt", format="nt")

    qres = g.query("""select * {
          ?subject ?predicate """ + double_quote(input_university) + """ . }""")

    for row in qres:
        university_list.append(int(row[1].split("/")[-1]))


    print "Year"

    qres = g.query("""select * {
              ?subject ?predicate """ + double_quote(input_year) + """ . }""")

    for row in qres:

        yrList.append(int(row[1].split("/")[-1]))

    matched_list = []

    for num in yrList:

        if num in university_list:
            matched_list.append(num)

    print len(matched_list)

    counter = 0
    for elem in (matched_list):
        subject = "http://www.crunchbased.org/degrees/{}".format(str(elem))
        qres = g.query("""select * {
                  <http://www.crunchbased.org/degrees/""" + str(elem) + """> ?predicate ?object}""")

        for row in qres:
            print row[0], row[1], subject



        counter = counter + 1
        print "Rank is {}".format(counter)
        print " "


