from gensim.test.utils import datapath
from gensim import utils
import gensim.models

class MyCorpus(object):
	"""An interator that yields sentences (lists of str)."""

	def __iter__(self):
		corpus_path = datapath('my_corps/bbs.cor')
		for line in open(corpus_path):
			# assume there's one document per line, tokens separated by whitespace
			yield utils.simple_preprocess(line)

if __name__ == '__main__':
	# sentences = MyCorpus()
	# print("start training...")
	# model = gensim.models.Word2Vec(sentences=sentences)
	# model.save("./baike3.model")
	model = gensim.models.Word2Vec.load('./bbs.model')
	print(model.wv.most_similar(positive=['棕榈油'], topn=20))
