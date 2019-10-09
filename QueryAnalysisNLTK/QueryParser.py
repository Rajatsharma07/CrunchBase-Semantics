import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.tree import Tree
from collections import defaultdict
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.stanford import StanfordPOSTagger

path_to_jar = './Masters-Passau/stanford-parser-full-2016-10-31/stanford-parser.jar'
path_to_models_jar = './Masters-Passau/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'

myNameEntity = []
myNounPhrases = []
myNounPhrasesTree = []
stopExtractingNP = False
count = 0

##### ------------ NER
print 'NER NLTK'

# Get Continous Chunk
def get_continuous_chunks(text):
    chunked = nltk.ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
            else:
                    continue
    return continuous_chunk

# Find Noun Phrases
def find_noun_phrases(tree):
    return [subtree for subtree in tree.subtrees(lambda t: t.label()=='NP')]

# Extract Chunks
def extract_chunks(tagged_sent, chunk_type):
    grp1, grp2, chunk_type = [], [], "-" + chunk_type
    for ind, (s, tp) in enumerate(tagged_sent):
        if tp.endswith(chunk_type):
            if not tp.startswith("B"):
                grp2.append(str(ind))
                grp1.append(s)
            else:
                if grp1:
                    yield " ".join(grp1), "-".join(grp2)
                grp1, grp2 = [s], [str(ind)]
    yield " ".join(grp1), "-".join(grp2)

# C Structure
def cStructure():
    print '######## C Structure'
    parser = StanfordParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    example = parser.raw_parse("Who were the CEO of IBM?")
#    example = parser.raw_parse("Steve Jobs was Founder of Apple. He was born in United States of America.")

    #for line in example:
        #for sentence in line:
            #sentence.draw()

    #print type(example)

    example = list(example)
    #print example
    abcabc = example[0]
    abcabc1 = abcabc[0]
    print type(abcabc)
    hello = str(abcabc)
    print type(abcabc)
    print hello
    #print abcabc1.label()

    for a in abcabc:
        #print a.height()
        if a.height() > 1:
            extractNP(a)


    print myNounPhrasesTree

def extractNP(parent):
    try:
        for child in parent:
            someStr = child.label().encode('utf8')
            if someStr == 'NP':
                extractNPLeaves(child)
                continue

            extractNP(child)
    except:
        doNothing = True

def extractNPLeaves(a):
    out_str = ''
    print a.leaves()
    for index in a.leaves():
        out_str += index + " "

    print out_str
    myNounPhrasesTree.append(out_str.encode('utf8'))

def dStructure():
    print 'Depencency Structure'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

    result = dependency_parser.raw_parse('Who were the CEO of IBM')
    dep = result.next()
    print list(dep.triples())

def posTagging():
    #myNounPhrases = []
    myCompletePOSStructure = []
    a = ['NNP', 'NNPS'] #Avoid NN,NNS. Only NNP , NNPS for purpose of NER.
    print '######## POS'
    english_postagger = StanfordPOSTagger(
        './Masters-Passau/stanford-postagger-full-2016-10-31/models/english-bidirectional-distsim.tagger',
        './Masters-Passau/stanford-postagger-full-2016-10-31/stanford-postagger.jar')
    #abc = english_postagger.tag('Steve Jobs was Founder of Apple. He was born in United States of America'.split())
    abc = english_postagger.tag('Who was the CEO of IBM'.split())
    print abc
    for number in abc:
        #print number[0],number[1]
        someTup = (number[0].encode('utf8'),number[1].encode('utf8'))
        #print someTup
        myCompletePOSStructure.append(someTup)

        #print split1[0] + ' ' + split1[1]
        #print unicodedata.normalize('NFKD', split1[0]).encode('ascii','ignore')
        #print unicodedata.normalize('NFKD', split1[1]).encode('ascii', 'ignore')

    print myCompletePOSStructure

    for number in abc:
        if any(x in number for x in a):
            #print number
            split1 = str(number).split(',')
            split2 = str(split1[0]).split('u')
            # print split2[1].replace("'", "")
            myNounPhrases.append(number)

    #print myNounPhrases

def NER():
    extractWords = ['ORGANIZATION', 'PERSON', 'LOCATION']
    #myNameEntity = []
    print '######## NER'
    st = StanfordNERTagger(
        './Masters-Passau/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz',
        './Masters-Passau/stanford-ner-2016-10-31/stanford-ner.jar')
    #temp = st.tag('Steve Jobs was Founder of Apple Inc. He was born in United States of America'.split())
    temp = st.tag('Who were the CEO of IBM'.split())
    print temp
    for number in temp:
        if any(x in number for x in extractWords):
            print number
            # split1 = str(number).split(',')
            # split2 = str(split1[0]).split('u')
            # print split2[1].replace("'", "")
            myNameEntity.append(number)

    print  "Exit NER"

def rest():
    sentence = "I am playing with Zohaib"
    sent1 = nltk.word_tokenize(sentence )
    sent2 = nltk.pos_tag(sent1)
    sent3 = nltk.ne_chunk(sent2, binary=True)
    print sent3
    #print sent3[2].leaves()

    #print get_continuous_chunks(sentence)

    sentences = nltk.sent_tokenize(sentence)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

def generateTreeForNP(sentence):
    #sentence = [('The', 'DT'), ('little', 'JJ'), ('yellow', 'JJ'), ('dog', 'NN'), ('barked', 'VBN'), ('at.', 'IN'), ('the', 'DT'), ('cat', 'NN')]
    sentence = [('Steve', 'NNP'), ('Jobs', 'NNP'), ('was', 'VBD'), ('Founder', 'NNP'), ('of', 'IN'), ('Apple.', 'NNP'), ('He', 'PRP'), ('was', 'VBD'), ('born', 'VBN'), ('in', 'IN'), ('United', 'NNP'), ('States', 'NNPS'), ('of', 'IN'), ('America', 'NNP')]

    grammar = "NP: {<DT>? <JJ>* <NN>* <NNS>* <NNP>* <NNPS>*}"
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)
    print(result)

def mergeSingleEntity():
    d = defaultdict(list)
    #print myNameEntity
    #print myNameEntity[0]
    mergedNameEntities = []
    mergedNameEntities.append(myNameEntity[0])
    for x in range(len(myNameEntity)-1):
        split1 = str(myNameEntity[x]).split(',')
        split2 = str(myNameEntity[x+1]).split(',')
        if split1[1] == split2[1]:
            print("Yes " + split1[1] + split2[1])




##### ------------ Depencency Structure
#dStructure()

##### ------------ POS Standford
#posTagging()
#print(myNounPhrases)
#generateTreeForNP("asd")

##### ------------ NER Standford
NER()
#mergeSingleEntity()
#print(myNameEntity)

##### ------------ C Structure (Getting Noun Phases)
#cStructure()

##### ------------ Add Remaining NNP,NNPS in NER list
#combineNPandNER()
