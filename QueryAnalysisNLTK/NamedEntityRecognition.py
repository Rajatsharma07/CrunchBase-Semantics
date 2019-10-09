import nltk
import re

# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# http://nlpforhackers.io/named-entity-extraction/
# https://www.eecis.udel.edu/~trnka/CISC889-11S/lectures/dongqing-chunking.pdn
# https://textblob.readthedocs.io/en/latest/
# http://stackoverflow.com/questions/37646254/keyword-phrase-extraction-from-free-text-using-nltk-and-python-for-structured-qu
# http://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/
# http://bdewilde.github.io/blog/2014/09/23/intro-to-automatic-keyphrase-extraction/
sentence = raw_input('Enter a rsearch: ')

print sentence

tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)
namedEnt =  nltk.ne_chunk(pos_tags) # , binary=m
print namedEnt
namedEnt.draw()

grammar = "NP: {<DT>?<JJ>*<NP>}"

cp = nltk.RegexpParser(grammar)
result = cp.parse(namedEnt)
print(result)

#print "Entities"
#entities = re.findall(r'NE\s(.*?)/',str(namedEnt))
#print entities


#IN = re.compile(r'.*\bin\b(?!\b.+ing)')
#for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
#    for rel in nltk.sem.extract_rels('ORG', 'LOC', doc,corpus='ieer', pattern = IN):
#        print(nltk.sem.rtuple(rel))


