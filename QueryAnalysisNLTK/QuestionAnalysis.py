from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.stanford import StanfordPOSTagger
from QueryAnalysisNLTK import reg
from nltk.corpus import stopwords
from AnswerAnalysis import cb_biography
import gensim
from QueryAnalysisNLTK import tripletSparql

# Load Google's pre-trained Word2Vec model.
#model = gensim.models.Word2Vec.load_word2vec_format('./Masters-Passau/GoogleNews-vectors-negative300.bin',binary=True)
#model.init_sims(replace=True)


standfordTagger = StanfordNERTagger(
      './Masters-Passau/stanford-ner-2016-10-31/classifiers/english.muc.7class.distsim.crf.ser.gz',
      './Masters-Passau/stanford-ner-2016-10-31/stanford-ner.jar')


path_to_jar = './Masters-Passau/stanford-parser-full-2016-10-31/stanford-parser.jar'
path_to_models_jar = './Masters-Passau/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'

cachedStopWords = stopwords.words("english")

# CrunchBased Mapping
cb_mapper = {'biography': False, 'history': False, "graduates" : False, "company" : False , "money": False, "acquired": False, "invested": False , "location" : False , "funds" :  False}

# Extracted Data from Questions

myNameEntity = []
myNounPhrases = []
myNounPhrasesTree = []
myVerbPhrasesTree = []
filtered_NounPhrases = []
filtered_VerbPhrases = []
gensim_word_list_noun = []
gensim_word_list_verb = []


## Question Analysis
qWord = None
np = None
vp = None
ner = {}

## Mappers , Word Net
nerTypes = ['ORGANIZATION', 'PERSON', 'LOCATION', 'DATE' , 'MONEY' , 'TIME']
ppl_life = ["history","life", "details", "biography" , "citizen", "story"]
graduates_net = ["alumnus", "alumna", "alum", "graduate", "grad", "graduates", "degree"]
title_net = ["ceo", "founder", "co-founder" , "managing director", "chairman", "vp", "president","cfo"]
office_net = ["company", "companionship", "fellowship", "society","society", "companies","office" , "business", "part" , "power"]
location_net = ["placement", "location", "located", "locating", "position", "positioning", "emplacement"]
company_net = ["company", "companionship", "fellowship", "society","society", "companies", "office" , "business", "part" , "power"]
funds_net = ["fund", "funded", "funds", "funding", "stock" , "investement", "store" , "finance", "finances", "cash", "cashed", "invest","induct","invested"]
money_net = ["money"]
acquire_net = ["acquires", "acquire" , "acquired", "get", "take" , "adapt" , "develop", "develope" , "grow"]



# C Structure - Noun Phrases
def cStructure(user_input):
#    print '######## C Structure ########'
    parser = StanfordParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    example = parser.raw_parse(user_input)
    example = list(example)
    #print example
    getTree = example[0]
#    print getTree

    getTreeTwo = getTree[0]
#    print getTreeTwo
#    print type(getTree)
    treeToString = str(getTree)
#    print type(treeToString)
#    print treeToString
    #print abcabc1.label()

    for element in getTree:
        #print a.height()
        if element.height() > 1:
            extractPhrases(element)

#    print myNounPhrasesTree


def extractPhrases(parent):
    try:
        for child in parent:
#            print "Children"
#            print child
            someStr = child.label().encode('utf8')
            if someStr == 'NP':
                extractPhrases(child)
                extractNPLeaves(child)
                continue
            if someStr == "VP":
#                print "Child VP"
#                print str(child)
                extractPhrases(child)
                extractVPLeaves(child)

            extractPhrases(child)
    except:
        doNothing = True


def extractNPLeaves(a):
#    print "Extract NP Leaves"
    out_str = ''
#    print a.leaves()
    for index in a.leaves():
#        print index
        out_str += index + " "

    out_str = out_str.strip()
#    print out_str
    myNounPhrasesTree.append(out_str.encode('utf8'))

def extractVPLeaves(child):
#    print "Extract VP Leaves"
    out_str = ''
#    print child.leaves()
    for index in child.leaves():
#        print index
        out_str += index + " "

    out_str = out_str.strip()
#    print out_str
    myVerbPhrasesTree.append(out_str.encode('utf8'))


def filterStopWords():
#    print "Filter Stop Words"
    for element in myNounPhrasesTree:
#        element = element.lower()
        element = ' '.join([word for word in element.split() if word not in cachedStopWords])
#        print element.upper()
        filtered_NounPhrases.append(element)

    for element in myVerbPhrasesTree:
    #        element = element.lower()
            element = ' '.join([word for word in element.split() if word not in cachedStopWords])
#            print element.upper()
            filtered_VerbPhrases.append(element)



def NerFromNp():
#    print "NER from NP"
    for word in myNounPhrasesTree:
#        print word
        user_inp = standfordTagger.tag(word.split())
#        print str(user_inp)

        for element in user_inp:

            if element[1] in nerTypes:
#                print "Type Found"
#                print element[0]
#                print element[1]
                #myNameEntity.append(element)
                if ner.get(element[1]) is None:
                    ner[element[1]] = element[0]
#                    print str(ner)
                else:
                    tmpner = ner.get(element[1])
#                    print type (tmpner.encode('utf8'))
#                    print type (element[1].encode('utf8'))
                    tmp = element[0].encode('utf8')
                    tmpner = tmpner.encode('utf8')
#                    print tmp
#                    print tmpner

                    if tmp in tmpner:
#                        print "Do Not Add Duplicate"
                        print ''
                    else:
                        tmpner = tmpner + " " + element[0]
                        ner[element[1]] = tmpner
 #                       print str(ner)


#    print "NER from VP"
    for word in myVerbPhrasesTree:
#        print word
        user_inp = standfordTagger.tag(word.split())
#        print str(user_inp)

        for element in user_inp:

            if element[1] in nerTypes:
                #                print "Type Found"
                #                print element[0]
                #                print element[1]
                # myNameEntity.append(element)
                if ner.get(element[1]) is None:
                    ner[element[1]] = element[0]
#                    print str(ner)
                else:
                    tmpner = ner.get(element[1])
                    #                    print type (tmpner.encode('utf8'))
                    #                    print type (element[1].encode('utf8'))
                    tmp = element[0].encode('utf8')
                    tmpner = tmpner.encode('utf8')
                    #                    print tmp
                    #                    print tmpner

                    if tmp in tmpner:
                        #                        print "Do Not Add Duplicate"
                        print ''
                    else:
                        tmpner = tmpner + " " + element[0]
                        ner[element[1]] = tmpner
 #                       print str(ner)


def nerAnalysis():
    print "NER Analysis"
    print str(ner)
    print " "


def npAnalysis():
    print "NP Analysis"
    global np
#    np = (filtered_NounPhrases[0]).lower()
    for word in filtered_NounPhrases:
#        print word
        if word in ner.values():
            print ''
 #           print "Do not assign ner values"
        else:
            np = word

        if np is not None:
            break
    print np
    print " "

def vpAnalysis():
    print "Vp Analysis"

    global vp
    for word in filtered_VerbPhrases:
#        print word
        wrdVplist = word.split()

        for element in wrdVplist:
            if element in ner.values():
                print ''
                print "Do not assign ner values"
            else:
                vp = element

            if vp is not None:
                break
    print vp
    print  " "


def question_controller():

    if np is not None:


       if np.lower() in title_net:

           tripletSparql.fetch_relationship_org(ner.get("ORGANIZATION"), gensim_word_list_noun)


       elif np.lower() in graduates_net:

           tripletSparql.fetch_graduates(ner.get("ORGANIZATION"), ner.get("DATE"), gensim_word_list_noun)

    elif vp is not None:
        print "vp"



def wordnetAnalysis():
    print "wordnet Analysis"

    wordnetSimilarWordsList = []

    for synset in wn.synsets('president'):
        print synset.lexname
        for lemma in synset.lemmas():
            print lemma.name()
            wordnetSimilarWordsList.append(lemma.name())


def gensimAnalysis():
    print "Gensim Analysis"

    # Load Google's pre-trained Word2Vec model.
    model = gensim.models.Word2Vec.load_word2vec_format(
        './Masters-Passau/GoogleNews-vectors-negative300.bin', binary=True)
    model.init_sims(replace=True)

    if np is not None:

        genlist =  model.most_similar(np)

        for similar in genlist:
            gensim_word_list_noun.append(similar[0])


    if vp is not None:

        genlist = model.most_similar(vp)

        for similar in genlist:
            gensim_word_list_verb.append(similar[0])


    del model


    print gensim_word_list_noun
    print " "




print "Project CrunchBase Semantics"
user_input = raw_input("Please enter your Question : ")
print "Question is : ", user_input
print " "


qWord = reg.latType(user_input)
cStructure(user_input)
NerFromNp()
filterStopWords()
nerAnalysis()
npAnalysis()
vpAnalysis()
gensimAnalysis()
question_controller()

