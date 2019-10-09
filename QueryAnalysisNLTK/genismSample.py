import gensim

# Load Google's pre-trained Word2Vec model.
#model = gensim.models.KeyedVectors.load_word2vec_format('./Masters-Passau/GoogleNews-vectors-negative300.bin', binary=True)
model = gensim.models.Word2Vec.load_word2vec_format('./Masters-Passau/GoogleNews-vectors-negative300.bin', binary=True)
#
model.init_sims(replace=True)
wrdlist =  model.most_similar('cfo')

for word in wrdlist:
    print word[0]

#word_vectors = model.wv
#del model

#print word_vectors.most_similar('graduate')